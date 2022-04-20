from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, Follow, Comment


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост. " * 10,
        )

    def test_models_have_correct_object_names_group(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        expected_object_title = group.title
        self.assertEqual(expected_object_title, "Тестовая группа")

    def test_models_have_correct_object_names_post(self):
        post = PostModelTest.post
        expected_object_text = post.text[:15]
        self.assertEqual(expected_object_text, ("Тестовый пост. " * 10)[:15])

    def test_verbose_name_group(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses_group = {
            "title": "Заголовок",
            "slug": "Ссылка",
            "description": "Описание",
        }
        for field, expected_value in field_verboses_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value
                )

    def test_verbose_name_post(self):
        """help_text для post в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses_post = {
            "text": "Текст",
            "pub_date": "Дата создания",
            "author": "Автор",
            "group": "Группа",
        }
        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text_post(self):
        """help_text для post в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            "text": "Текст поста",
            "group": "Добавить пост в группу",
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user_one = cls.users.objects.create_user(username="AuthOne")
        cls.user_two = cls.users.objects.create_user(username="AuthTwo")

    def setUp(self):
        self.follow = Follow.objects.create(user=self.user_one,
                                            author=self.user_two)

    def test_verbose_name_post(self):
        """help_text для Follow в полях совпадает с ожидаемым."""
        field_verboses_post = {
            "author": "Автор",
            "user": "Подписчик",
        }
        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.follow._meta.get_field(
                        field).verbose_name, expected_value
                )

    def test_add_new_following(self):
        '''Проверка на добавление нового подписчика'''
        self.assertEqual(self.follow.user,
                         FollowModelTest.user_one)
        self.assertEqual(self.follow.author,
                         FollowModelTest.user_two)

    def test_unfollowing(self):
        '''Проверка отписки'''
        self.follow.delete()
        self.assertEqual(Follow.objects.count(), 0)


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.user = cls.users.objects.create_user(username="Auth")

    def setUp(self):
        self.post = Post.objects.create(
            author=self.user,
            text="Тестовый пост",
        )
        self.add_comment = Comment.objects.create(author=self.user,
                                                  post=self.post,
                                                  text='Тестовый коммент')

    def test_verbose_name_post(self):
        """help_text для Follow в полях совпадает с ожидаемым."""
        field_verboses_post = {
            "author": "Автор",
            "post": "Пост",
            "text": "Комментарий",
        }
        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.add_comment._meta.get_field(
                        field).verbose_name, expected_value
                )

    def test_comment_and_delite(self):
        '''Проверка нового поста и удаление'''
        post = Post.objects.create(
            author=CommentModelTest.user,
            text="Тестовый пост 2",
        )
        self.assertEqual(self.add_comment.author,
                         CommentModelTest.user)
        self.assertEqual(self.add_comment.post,
                         self.post)
        self.assertEqual(Comment.objects.filter(post=post).count(), 0)
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
        self.add_comment.delete()
        self.assertEqual(Comment.objects.count(), 0)
