import shutil

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User

INDEX_URLS = reverse('index')
NEW_POST_URLS = reverse('new_post')
MESS_TEMPLATE_HTML = 'шаблон {} не соответствует адресу {}'
MESS_CONTEXT_FAIL = 'context некорректно передается в шаблон {}'
MESS_POST_FAIL = 'проверь размещение постов на странице {}'
MESS_PAGINAOR = 'проверьте работу пагинатора'
PG_PAG = '?page=2'
F_POST_COUNT = 10
S_POST_COUNT = 3
TEST_TEXT_DESCRIP = 'Тестовый текст'
TEST_TEXT_SLUG = 'test-group'
TEST_TEXT_1 = '№ 1 Запись тестовой задачи'
TEST_TEXT_2 = '№ 2 Запись тестовой задачи'
INDEX_TEMPLATE = 'posts/index.html'
GROUP_TEMPLATE = 'posts/group.html'
NEW_POST_TEMPLATE = 'posts/new.html'
COMMENT_TEMPLATE = 'includes/comments.html'
USER_NAME_1_AUTH = 'leo'
USER_NAME_2 = 'John'
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B')
UPLOADED = SimpleUploadedFile(
    name='small.gif',
    content=SMALL_GIF,
    content_type='image/gif')


class GroupPostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username=USER_NAME_1_AUTH)
        cls.user2 = User.objects.create_user(username=USER_NAME_2)
        cls.group1 = Group.objects.create(
            title=cls.user1,
            description=TEST_TEXT_DESCRIP,
            slug=cls.user1)
        cls.post1 = Post.objects.create(
            text=TEST_TEXT_1,
            author=cls.user1,
            group=cls.group1,
            image=UPLOADED)
        cls.post2 = Post.objects.create(
            text=TEST_TEXT_2,
            author=cls.user2,
            group=Group.objects.create(
                title=cls.user2,
                description=TEST_TEXT_DESCRIP,
                slug=cls.user2),
            image=UPLOADED)
        cls.GROUP_1_URLS = reverse(
            'group_posts',
            kwargs={'slug': cls.user1})
        cls.GROUP_2_URLS = reverse(
            'group_posts',
            kwargs={'slug': cls.user2})
        cls.EDIT_POST_URLS = reverse(
            'edit_post',
            kwargs={'username': cls.user1, 'post_id': cls.post1.id})
        cls.PROFILE_URLS = reverse(
            'profile',
            kwargs={'username': cls.user1})
        cls.POST_URLS = reverse(
            'post',
            kwargs={'username': cls.user1, 'post_id': cls.post1.id})
        cls.COMMENT_URLS = reverse(
            'add_comment',
            kwargs={'username': cls.user1, 'post_id': cls.post1.id})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorixed_client = Client()
        self.authorixed_client.force_login(self.user1)

    def test_name_use_correct_template(self):
        """
        Вызываются ли для страниц ожидаемые шаблоны через name.
        """
        templates_url_names = {
            INDEX_URLS: INDEX_TEMPLATE,
            self.GROUP_1_URLS: GROUP_TEMPLATE,
            NEW_POST_URLS: NEW_POST_TEMPLATE,
            self.COMMENT_URLS: COMMENT_TEMPLATE}

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorixed_client.get(adress)
                self.assertTemplateUsed(
                    response, template,
                    MESS_TEMPLATE_HTML.format(template, adress))

    def test_index_shows_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон index.
        """
        response = self.authorixed_client.get(INDEX_URLS)
        context_list = {
            response.context['page'].object_list[0]:
                Post.objects.first(),
            response.context['page'].object_list[0].image:
                Post.objects.first().image}
        for fields, value in context_list.items():
            with self.subTest(value=value):
                self.assertEqual(
                    fields,
                    value,
                    MESS_CONTEXT_FAIL.format(INDEX_URLS))

    def test_group_shows_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон group_posts.
        """
        response = self.authorixed_client.get(self.GROUP_1_URLS)
        context_list = {
            response.context['group'].title:
                str(self.group1.title),
            response.context['group'].description:
                str(self.group1.description),
            response.context['group'].slug:
                str(self.group1.slug),
            response.context['page'].object_list[0]:
                self.post1,
            response.context['page'].object_list[0].image:
                self.post1.image}
        for fields, value in context_list.items():
            with self.subTest(value=value):
                self.assertEqual(
                    fields,
                    value,
                    MESS_CONTEXT_FAIL.format(self.GROUP_1_URLS))

    def test_new_post_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон new_post.
        """
        response = self.authorixed_client.get(NEW_POST_URLS)
        form_fields_names = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields_names.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(
                    form_field,
                    expected,
                    MESS_CONTEXT_FAIL.format(NEW_POST_URLS))

    def test_edit_post_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон edit_post.
        """
        response = self.authorixed_client.get(self.EDIT_POST_URLS)
        form_pages_names = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_pages_names.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(
                    form_field,
                    expected,
                    MESS_CONTEXT_FAIL.format(self.EDIT_POST_URLS))

    def test_profile_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон profile.
        """
        response = self.authorixed_client.get(self.PROFILE_URLS)
        form_pages_names = {
            response.context['author'].username:
                str(self.user1),
            response.context['current_path']:
                str(self.PROFILE_URLS),
            response.context['page'].object_list[0].image:
                self.post1.image}
        for value, expected in form_pages_names.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value,
                    expected,
                    MESS_CONTEXT_FAIL.format(self.PROFILE_URLS))

    def test_post_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон post.
        """
        response = self.authorixed_client.get(self.POST_URLS)
        form_pages_names = {
            response.context['author'].username: str(self.user1),
            response.context['current_path']: str(self.POST_URLS),
            response.context['post'].text: self.post1.text,
            response.context['post'].image: self.post1.image}
        for value, expected in form_pages_names.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value,
                    expected,
                    MESS_CONTEXT_FAIL.format(self.POST_URLS))

    def test_new_post_correct_index_and_group(self):
        """
        Пост на странице index, на выбр. group.
        и отсутсв в невыбраной группе
        """
        urls_list = {
            self.GROUP_1_URLS: self.authorixed_client.get(self.GROUP_1_URLS),
            INDEX_URLS: self.authorixed_client.get(INDEX_URLS)}
        for adress, value in urls_list.items():
            with self.subTest(adress=adress):
                self.assertIn(
                    self.post1,
                    value.context['page'].object_list,
                    MESS_POST_FAIL.format(adress))
        response = self.authorixed_client.get(self.GROUP_2_URLS)
        self.assertNotIn(
            self.post1,
            response.context['page'].object_list,
            MESS_POST_FAIL.format(self.GROUP_2_URLS))

    def test_comment_correct_context(self):
        """
        Cответствует словарь context, передаваемый в шаблон add_comment.
        """
        response = self.authorixed_client.get(self.COMMENT_URLS)
        form_fields_names = {'text': forms.fields.CharField}
        for value, expected in form_fields_names.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(
                    form_field,
                    expected,
                    MESS_CONTEXT_FAIL.format(self.COMMENT_URLS))


class CashViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_NAME_1_AUTH)
        cls.post = Post.objects.create(
            text=TEST_TEXT_1,
            author=cls.user,
            image=UPLOADED)
        cls.post2 = Post.objects.create(
            text=TEST_TEXT_2,
            author=cls.user,
            image=UPLOADED)

    def setUp(self):
        self.authorixed_client = Client()
        self.authorixed_client.force_login(self.user)

    def test_cash_index(self):
        """
        Проверка кеширования главной страницы.
        """
        response = self.authorixed_client.get(INDEX_URLS)
        content_1 = response.content
        Post.objects.get(id=self.post.id).delete()
        self.assertEqual(
            content_1,
            response.content,
            MESS_CONTEXT_FAIL.format(INDEX_URLS))


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_NAME_2)
        cls.group = Group.objects.create(
            title=USER_NAME_2,
            description=TEST_TEXT_DESCRIP,
            slug=TEST_TEXT_SLUG)
        objs = (Post(
            text=TEST_TEXT_1 + str(i),
            author=cls.user,
            group=cls.group) for i in range(13))
        Post.objects.bulk_create(objs)
        cls.GROUP_URLS = reverse(
            'group_posts',
            kwargs={'slug': cls.group.slug})

    def setUp(self):
        self.guest_client = Client()
        cache.clear()

    def test_first_page_contains_ten_records_index_group(self):
        """
        Проверка количества постов на cтранице пагинатора.
        """
        list_urls = {
            self.guest_client.get(INDEX_URLS): F_POST_COUNT,
            self.guest_client.get(self.GROUP_URLS): F_POST_COUNT,
            self.guest_client.get(INDEX_URLS + PG_PAG): S_POST_COUNT,
            self.guest_client.get(self.GROUP_URLS + PG_PAG): S_POST_COUNT}
        for value, expected in list_urls.items():
            with self.subTest(value=value):
                self.assertEqual(
                    len(value.context['page'].object_list),
                    expected,
                    MESS_PAGINAOR)
