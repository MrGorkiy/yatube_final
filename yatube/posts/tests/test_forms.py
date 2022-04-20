import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Comment, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

POST_CREATE_PAGE = reverse("posts:post_create")


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="auth")

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст",
        )
        cls.PAGE_AUTHOR = reverse(
            "posts:profile", kwargs={"username": cls.user}
        )
        cls.POST_EDIT = reverse(
            "posts:post_edit", kwargs={"post_id": cls.post.pk}
        )
        cls.POST_CREATE_COMMENT = reverse(
            "posts:add_comment", kwargs={"post_id": cls.post.pk}
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        """Создание поста аторизированым пользователем на сайте."""
        tasks_count = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Тестовый текст 1",
            "image": uploaded,
        }
        response = self.authorized_client.post(
            POST_CREATE_PAGE, data=form_data, follow=True
        )
        self.assertRedirects(response, TaskCreateFormTests.PAGE_AUTHOR)
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text="Тестовый текст 1", image="posts/small.gif"
            ).exists()
        )

    def test_edit_post(self):
        """Редактирование поста аторизированым пользователем на сайте."""
        form_data = {
            "text": "Редактированый пост",
        }
        response = self.authorized_client.post(
            TaskCreateFormTests.POST_EDIT,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail",
                kwargs={"post_id": TaskCreateFormTests.post.pk},
            ),
        )
        self.assertTrue(
            Post.objects.filter(
                pk=TaskCreateFormTests.post.pk, text="Редактированый пост"
            ).exists()
        )

    def test_add_comment_post(self):
        """Добавление комментария авторизированым пользователем."""
        form_data = {
            "text": "Первый комментарий",
        }
        response = self.authorized_client.post(
            TaskCreateFormTests.POST_CREATE_COMMENT,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                "posts:post_detail",
                kwargs={"post_id": TaskCreateFormTests.post.pk},
            ),
        )
        self.assertTrue(
            Comment.objects.filter(
                post=TaskCreateFormTests.post,
                text="Первый комментарий",
                author=TaskCreateFormTests.user,
            ).exists()
        )
