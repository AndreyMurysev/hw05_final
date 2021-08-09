from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post, User

MESS_AUTH_US = 'зарег. польз.'
MESS_NOT_AUTH_US = 'неавтор. польз.'
MESS_PAGE_USER = 'страница не отображается по адресу "{}" для {}'
MESS_TEMPLATE_HTML = 'шаблон {} не соответствует адресу {}'
INDEX_URLS = '/'
GROUP_URLS = '/group/{}/'
NEW_URLS = '/new/'
PROFILE_URLS = '/{}/'
POST_URLS = '/{}/{}/'
EDIT_URLS = '/{}/{}/edit/'
COMMENTS_URLS = '/{}/{}/comment/'
ST_CODE_1 = 200
ST_CODE_2 = 302
ST_CODE_3 = 404
TEST_TEXT_DESCRIP = 'Тестовый текст'
TEST_TEXT = '№ 1 Запись тестовой задачи'
INDEX_TEMPLATE = 'posts/index.html'
GROUP_TEMPLATE = 'posts/group.html'
NEW_POST_TEMPLATE = 'posts/new.html'
TEMPLATE_404 = 'misc/404.html'
USER_NAME_1_AUTH = 'leo'
USER_NAME_2_AUTH = 'John'
USER_NAME_3 = 'Roi'


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username=USER_NAME_1_AUTH)
        cls.user2 = User.objects.create_user(username=USER_NAME_2_AUTH)
        cls.group = Group.objects.create(
            title=cls.user1,
            description=TEST_TEXT_DESCRIP,
            slug=cls.user1)
        cls.post = Post.objects.create(
            text=TEST_TEXT,
            author=cls.user1)

    def setUp(self):
        self.guest_client = Client()
        self.authorixed_client = Client()
        self.authorixed_client2 = Client()
        self.authorixed_client.force_login(self.user1)
        self.authorixed_client2.force_login(self.user2)
        cache.clear()

    def test_urls_uses_correct_template(self):
        """
        Проверка, вызываются ли для страниц ожидаемые шаблоны.
        """
        templates_url_names = {
            INDEX_URLS: INDEX_TEMPLATE,
            GROUP_URLS.format(self.user1): GROUP_TEMPLATE,
            NEW_URLS: NEW_POST_TEMPLATE,
            EDIT_URLS.format(self.user1, self.post.id): NEW_POST_TEMPLATE,
            PROFILE_URLS.format(USER_NAME_3): TEMPLATE_404}

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorixed_client.get(adress)
                self.assertTemplateUsed(
                    response, template,
                    MESS_TEMPLATE_HTML.format(template, adress))

    def test_index_group_new_profile_post_id(self):
        """
        Доступность страниц для пользователей.
        """
        list_urls = [
            {INDEX_URLS:
                [self.guest_client, ST_CODE_1, MESS_NOT_AUTH_US]},
            {GROUP_URLS.format(self.user1):
                [self.guest_client, ST_CODE_1, MESS_NOT_AUTH_US]},
            {NEW_URLS:
                [self.guest_client, ST_CODE_2, MESS_NOT_AUTH_US]},
            {PROFILE_URLS.format(self.user1):
                [self.guest_client, ST_CODE_1, MESS_NOT_AUTH_US]},
            {POST_URLS.format(self.user1, self.post.id):
                [self.guest_client, ST_CODE_1, MESS_NOT_AUTH_US]},
            {EDIT_URLS.format(self.user1, self.post.id):
                [self.guest_client, ST_CODE_2, MESS_NOT_AUTH_US]},
            {COMMENTS_URLS.format(self.user1, self.post.id):
                [self.guest_client, ST_CODE_2, MESS_NOT_AUTH_US]},
            {INDEX_URLS:
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {GROUP_URLS.format(self.user1):
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {NEW_URLS:
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {PROFILE_URLS.format(self.user1):
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {POST_URLS.format(self.user1, self.post.id):
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {EDIT_URLS.format(self.user1, self.post.id):
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]},
            {EDIT_URLS.format(self.user1, self.post.id):
                [self.authorixed_client2, ST_CODE_2, MESS_AUTH_US]},
            {PROFILE_URLS.format(USER_NAME_3):
                [self.authorixed_client2, ST_CODE_3, MESS_AUTH_US]},
            {COMMENTS_URLS.format(self.user1, self.post.id):
                [self.authorixed_client, ST_CODE_1, MESS_AUTH_US]}]

        for element_mass in list_urls:
            for adress, st_code in element_mass.items():
                with self.subTest(adress=adress):
                    response = st_code[0].get(adress)
                    self.assertEqual(
                        response.status_code,
                        st_code[1],
                        MESS_PAGE_USER.format(adress, st_code[2]))
