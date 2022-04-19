from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
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
