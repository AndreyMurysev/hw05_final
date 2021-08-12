from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()

AUTHOR_URLS = '/about/author/'
TECH_URLS = '/about/tech/'
MESS_TEMPLATE_HTML = 'шаблон {} не соответствует адресу {}'
MESS_PAGE_USER = 'страница не отображается по адресу "{}"'
ST_CODE_1 = 200
USER_NAME = 'John'
AUTHOR_TEMPLATE = 'about/author.html'
TECH_TEMPLATE = 'about/tech.html'


class AboutTestsUrls(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=USER_NAME)
        self.authorixed_client = Client()
        self.authorixed_client.force_login(self.user)

    def test_name_use_correct_template(self):
        """
        Вызываются ли для страниц ожидаемые шаблоны через URLS.
        """
        templates_url_names = {
            AUTHOR_URLS: AUTHOR_TEMPLATE,
            TECH_URLS: TECH_TEMPLATE}

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorixed_client.get(adress)
                self.assertTemplateUsed(
                    response, template,
                    MESS_TEMPLATE_HTML.format(template, adress))

    def test_shows_urls_guest_client(self):
        """
        Cтраницы /about/author/ и /about/tech/ доступны пользователям по URLS.
        """
        html_urls = {
            self.guest_client.get(AUTHOR_URLS): ST_CODE_1,
            self.guest_client.get(TECH_URLS): ST_CODE_1,
            self.authorixed_client.get(AUTHOR_URLS): ST_CODE_1,
            self.authorixed_client.get(TECH_URLS): ST_CODE_1}
        for urls, value in html_urls.items():
            with self.subTest(urls=urls):
                self.assertEqual(
                    urls.status_code,
                    value,
                    MESS_PAGE_USER.format(urls))
