from django.test import TestCase

from ..models import Group, Post, User

MESS_POST = 'представление title в виде названия группы'
MESS_GROUP = 'представление text в виде пятнадцати символов поста:'
TEST_TEXT_TITLE = 'Заголовок тестовой задачи'
TEST_TEXT_DESCRIP = 'Тестовый текст'
TEST_TEXT_SLUG = 'test-group'
TEST_TEXT = 'Запись тестовой задачи'
USER_NAME = 'John'


class GroupPostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=TEST_TEXT_TITLE,
            description=TEST_TEXT_DESCRIP,
            slug=TEST_TEXT_SLUG)
        cls.post = Post.objects.create(
            text=TEST_TEXT,
            author=User.objects.create_user(username=USER_NAME))

    def test_verbose_name(self):
        """
        Проверка __str__ класса Post приложения posts.
        """
        group = self.group
        verbose = group.title
        self.assertEqual(
            verbose,
            self.group.title,
            MESS_GROUP)

    def text_value_post(self):
        """
        Проверка __str__ класса Group приложения posts..
        """
        post = self.post
        value = post.text[:15]
        self.assertEqual(
            value,
            str(post),
            MESS_POST)
