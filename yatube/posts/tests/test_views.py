import tempfile
import shutil

from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from django.conf import settings
from ..models import Group, Post, Follow

INDEX_PAGE = reverse("posts:index")
FOLLOWER_PAGE = reverse("posts:follow_index")
POST_CREATE_PAGE = reverse("posts:post_create")
PAGE_GROUP = reverse("posts:group_list", kwargs={"slug": "test-slug-group"})
PAGE_GROUP2 = reverse("posts:group_list", kwargs={"slug": "nool-slug-group"})

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskPagesTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="auth")
        cls.author = cls.users.objects.create_user(username="NewUser")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug-group",
            description="Тестовое описание",
        )

        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый текст",
            image=uploaded,
        )
        cls.PAGE_AUTHOR = (
            reverse("posts:profile", kwargs={"username": cls.user}))
        cls.POST_DETALS = (
            reverse("posts:post_detail", kwargs={"post_id": cls.post.pk}))
        cls.POST_EDIT = (
            reverse("posts:post_edit", kwargs={"post_id": cls.post.pk}))
        cls.POST_CREATE_COMMENT = (reverse("posts:add_comment",
                                           kwargs={"post_id": cls.post.pk}))
        cls.FOLLOW = (reverse("posts:profile_follow",
                              kwargs={"username": cls.author}))
        cls.UNFOLLOW = (reverse("posts:profile_unfollow",
                                kwargs={"username": cls.author}))

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Модуль shutil - библиотека Python с удобными инструментами
        # для управления файлами и директориями:
        # создание, удаление, копирование, перемещение, изменение папок и файлов
        # Метод shutil.rmtree удаляет директорию и всё её содержимое
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_pages_uses_correct_template(self):
        """Проверка namespace:name."""
        templates_pages_names = {
            INDEX_PAGE: "posts/index.html",
            PAGE_GROUP: "posts/group_list.html",
            TaskPagesTests.PAGE_AUTHOR: "posts/profile.html",
            TaskPagesTests.POST_DETALS: "posts/post_detail.html",
            POST_CREATE_PAGE: "posts/create_post.html",
            TaskPagesTests.POST_EDIT: "posts/create_post.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_post_page_show_correct_context(self):
        """Проверка контекста формы создания поста."""
        response = self.authorized_client.get(POST_CREATE_PAGE)
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        """Проверка контекста формы редактирования поста."""
        response = self.authorized_client.get(TaskPagesTests.POST_EDIT)
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get("form").fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_detail_pages_show_correct_context(self):
        """Проверка контекста страницы с постом."""
        response = self.authorized_client.get(TaskPagesTests.POST_DETALS)
        self.assertEqual(response.context.get("post").author, self.user)
        self.assertEqual(response.context.get("post").text, "Тестовый текст")
        self.assertEqual(response.context.get("post").pk, 1)
        self.assertEqual(response.context.get("post").image, 'posts/small.gif')

    def test_profile_user_pages_show_correct_context(self):
        """Проверка контекста страницы пользователя."""
        response = self.authorized_client.get(TaskPagesTests.PAGE_AUTHOR)
        objects = len(response.context["page_obj"])
        first_object = response.context["page_obj"][0]
        self.assertEqual(objects, 1)
        self.assertEqual(first_object.image, 'posts/small.gif')

    def test_group_list_page_show_correct_context(self):
        """Проверка контекста страницы группы постов."""
        uploaded = SimpleUploadedFile(
            name='smalls.gif',
            content=TaskPagesTests.small_gif,
            content_type='image/gif'
        )
        post = Post.objects.create(
            author=self.user,
            text="Тестовый текст",
            group=TaskPagesTests.group,
            image=uploaded,
        )

        response = self.authorized_client.get(PAGE_GROUP)
        first_object = response.context["page_obj"][0]
        task_group_0 = first_object.group.title
        task_text_0 = first_object.text
        task_pk_0 = first_object.pk
        self.assertEqual(task_group_0, "Тестовая группа")
        self.assertEqual(task_text_0, "Тестовый текст")
        self.assertEqual(task_pk_0, post.pk)
        self.assertEqual(first_object.image, 'posts/smalls.gif')

    def test_new_post_for_index_page_contains(self):
        """Проверяем главную на наличие нового поста"""
        uploaded = SimpleUploadedFile(
            name='small_index.gif',
            content=TaskPagesTests.small_gif,
            content_type='image/gif'
        )
        post = Post.objects.create(
            author=self.user,
            text="Тестовый текст 2",
            group=TaskPagesTests.group,
            image=uploaded,
        )

        response = self.authorized_client.get(INDEX_PAGE)
        first_object = response.context["page_obj"][0]
        task_pk = first_object.pk
        task_text = first_object.text
        self.assertEqual(task_text, "Тестовый текст 2")
        self.assertEqual(task_pk, post.pk)
        self.assertEqual(first_object.group.title, "Тестовая группа")
        self.assertEqual(first_object.image, 'posts/small_index.gif')

    def test_cache_index(self):
        """Проверяем работу кеша главной страницы"""
        response_1 = self.authorized_client.get(INDEX_PAGE)
        first_object = response_1.context['page_obj'][0]
        post_bytes_text = first_object.text.encode('utf-8')

        # удалить запись
        first_object.delete()
        # проверить доступность записи (из кеша)
        response_2 = self.authorized_client.get(INDEX_PAGE)
        self.assertIn(post_bytes_text, response_2.content)
        # очистить кеш
        cache.clear()
        response_3 = self.authorized_client.get(INDEX_PAGE)
        # проверить изменение записи
        self.assertNotIn(post_bytes_text, response_3.content)

    def test_follow_and_unfollow(self):
        '''Проверяем работу подписки и отписки авторизированым пользователем'''
        self.authorized_client.get(TaskPagesTests.FOLLOW)
        following = Follow.objects.filter(author=TaskPagesTests.author,
                                          user=TaskPagesTests.user).all()
        self.assertEqual(following.count(), 1)

        self.authorized_client.get(TaskPagesTests.UNFOLLOW)
        following_unsub = Follow.objects.filter(author=TaskPagesTests.author,
                                          user=TaskPagesTests.user).all()
        self.assertEqual(following_unsub.count(), 0)

    def test_follow_add_post_test(self):
        unsubber = TaskPagesTests.users.objects.create_user(username="UnSuber")
        authorized_clients = Client()
        authorized_clients.force_login(unsubber)
        self.authorized_client.get(TaskPagesTests.FOLLOW)
        post = Post.objects.create(
            author=self.author,
            text="Тестовый текст 2",
        )
        response_sub = self.authorized_client.get(FOLLOWER_PAGE)
        first_object = response_sub.context["page_obj"][0]
        task_pk = first_object.pk
        task_text = first_object.text
        self.assertEqual(task_text, "Тестовый текст 2")
        self.assertEqual(task_pk, post.pk)

        response_sub = authorized_clients.get(FOLLOWER_PAGE)
        first_object = response_sub.context["page_obj"]
        self.assertEqual(len(first_object), 0)



class PagesPajiginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="NoName")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug-group",
            description="Тестовое описание",
        )
        for n in range(13):
            Post.objects.create(
                author=cls.user,
                text="Тестовый текст",
            )
        for n in range(14, 17):
            Post.objects.create(
                author=cls.user,
                text=f"Тестовый текст {n}",
                group=cls.group,
            )

    def setUp(self):
        self.user = PagesPajiginatorTests.users.objects.create_user(
            username="HasNoName")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page_contains_ten_records(self):
        """Проверка 1 страницы паджинатора главной страницы"""
        response = self.authorized_client.get(INDEX_PAGE)
        self.assertEqual(len(response.context["page_obj"]),
                         settings.PAGINATOR_COUNT)

    def test_index_next_page_contains_six_records(self):
        """Проверка 2 страницы паджинатора главной страницы"""
        response = self.authorized_client.get(
            INDEX_PAGE + "?page=2"
        )
        self.assertEqual(len(response.context["page_obj"]), 6)

    def test_group_list_page_show_correct_context(self):
        """Прверка страницы группы на правильный контекст"""
        response = self.authorized_client.get(PAGE_GROUP)
        self.assertEqual(len(response.context["page_obj"]), 3)


class CreatPost(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug-group",
            description="Тестовое описание",
        )
        cls.new_group = Group.objects.create(
            title="Пустая группа",
            slug="nool-slug-group",
            description="В эту группу посты не добавлены",
        )
        Post.objects.create(
            author=cls.user,
            text="Тестовый текст 0",
            group=cls.group,
        )
        cls.PAGE_AUTHOR = (
            reverse("posts:profile", kwargs={"username": cls.user}))

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_for_index_page(self):
        """Проверяем добавление нового поста на главную страницу"""
        response = self.authorized_client.get(INDEX_PAGE)
        first_object = response.context["page_obj"][0]
        self.assertEqual(first_object.text, "Тестовый текст 0")
        self.assertEqual(first_object.pk, 1)

    def test_group_list_page_show_correct_context(self):
        """Проверка добавление нового поста в выбранную группу"""
        response = self.authorized_client.get(PAGE_GROUP)
        res_group2 = self.authorized_client.get(PAGE_GROUP2)
        first_object = response.context["page_obj"][0]
        self.assertEqual(first_object.group.title, "Тестовая группа")
        self.assertEqual(first_object.text, "Тестовый текст 0")
        self.assertEqual(first_object.pk, 1)
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(len(res_group2.context["page_obj"]), 0)

    def test_profile_user_pages_show_correct_context(self):
        """Проверка добавление нового поста в выбранного пользователя."""
        response = self.authorized_client.get(CreatPost.PAGE_AUTHOR)
        objects = response.context["page_obj"]
        self.assertEqual(len(objects), 1)
