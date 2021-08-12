import textwrap

from django.test import Client, TestCase

from ..models import Follow, Comment, Group, Post, User

MESS = 'проверьте представления в models'
TEST_TEXT_TITLE = 'Заголовок тестовой задачи'
TEST_TEXT_DESCRIP = 'Тестовый текст'
TEST_TEXT_SLUG = 'test-group'
TEST_TEXT = 'Запись тестовой задачи'
USER_NAME = 'John'
USER_NAME_2 = 'Roi'


class GroupPostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_NAME)
        cls.user2 = User.objects.create_user(username=USER_NAME_2)
        cls.group = Group.objects.create(
            title=TEST_TEXT_TITLE,
            description=TEST_TEXT_DESCRIP,
            slug=TEST_TEXT_SLUG)
        cls.post = Post.objects.create(
            text=TEST_TEXT,
            author=cls.user)
        cls.comment = Comment.objects.create(
            text=TEST_TEXT,
            author=cls.user,
            post=cls.post)
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.user2)

    def setUp(self):
        self.guest_client = Client()
        self.authorixed_client = Client()
        self.authorixed_client2 = Client()
        self.authorixed_client.force_login(self.user)
        self.authorixed_client2.force_login(self.user2)

    def test_str_models(self):
        """
        Проверка __str__ models приложения posts.
        """
        list_str = {
            str(self.group): self.group.title,
            str(self.post): textwrap.shorten(self.post.text, width=15),
            str(self.comment): textwrap.shorten(self.comment.text, width=15),
            str(self.follow): str(self.follow.user)}
        for key, value in list_str.items():
            with self.subTest(value=value):
                self.assertEqual(key, value, MESS)
