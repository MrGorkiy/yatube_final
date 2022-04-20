from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

PAGE_INDEX = "/"
PAGE_INDEX_FOLLOW = "/follow/"
PAGE_GROUP = "/group/test-slug-group/"
PAGE_POST = "/posts/1/"
PAGE_POST_EDIT = "/posts/1/edit/"
PAGE_CREATE = "/create/"
PAGE_USER_PROFILE = "/profile/NoName/"
PAGE_UNEXISTING = "/unexisting_page/"
PAGE_ADD_COMMENTS = "/posts/1/comment/"


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.users = get_user_model()
        cls.guest_client = Client()
        cls.user = cls.users.objects.create_user(username="NoName")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug-group",
            description="Тестовое описание",
        )
        Post.objects.create(
            author=cls.user,
            text="Тестовый текст",
            pk="1",
            group=cls.group,
        )

    def test_urls_guest_client_status_url(self):
        """Доступность страниц любому пользователю."""
        templates_url_status = {
            PAGE_INDEX: HTTPStatus.OK,
            PAGE_GROUP: HTTPStatus.OK,
            PAGE_POST: HTTPStatus.OK,
            PAGE_POST_EDIT: HTTPStatus.FOUND,
            PAGE_CREATE: HTTPStatus.FOUND,
            PAGE_USER_PROFILE: HTTPStatus.OK,
            PAGE_UNEXISTING: HTTPStatus.NOT_FOUND,
            PAGE_ADD_COMMENTS: HTTPStatus.FOUND,
            PAGE_INDEX_FOLLOW: HTTPStatus.FOUND,
        }
        for address, status in templates_url_status.items():
            with self.subTest(address=address):
                response = TaskURLTests.guest_client.get(address)
                self.assertEqual(response.status_code, status)

    def test_urls_guest_client_correct_template(self):
        """
        URL-адрес использует соответствующий шаблон для
        неавторизированного пользователя.
        """
        templates_url_names = {
            PAGE_INDEX: "posts/index.html",
            PAGE_GROUP: "posts/group_list.html",
            PAGE_POST: "posts/post_detail.html",
            PAGE_USER_PROFILE: "posts/profile.html",
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = TaskURLTests.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_authorized_client_correct_template(self):
        """
        URL-адрес использует соответствующий шаблон для
        авторизированного пользователя.
        """
        templates_url_names = {
            PAGE_INDEX: "posts/index.html",
            PAGE_GROUP: "posts/group_list.html",
            PAGE_POST: "posts/post_detail.html",
            PAGE_POST_EDIT: "posts/create_post.html",
            PAGE_CREATE: "posts/create_post.html",
            PAGE_USER_PROFILE: "posts/profile.html",
            PAGE_INDEX_FOLLOW: "posts/follow.html",
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = TaskURLTests.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
