import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Comment, Post, User

INDEX_URLS = reverse('index')
NEW_POST_URLS = reverse('new_post')
MESS_NEW_POST = 'пост не создан'
MESS_COUNT_POST = 'количество постов должно быть {}'
MESS_COUNT_COMMENT = 'количество комментариев должно быть {}'
MESS_EDIT_POST = 'пост не отредактирован'
TEST_TEXT_1 = 'Тестовый текст'
TEST_TEXT_2 = 'Тестовый текст33'
TEST_TEXT_3 = 'Текст комментария'
USER_NAME = 'Helen'
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
URL_IMAGE = 'posts/small.gif'


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER_NAME)
        cls.post = Post.objects.create(
            text=TEST_TEXT_1,
            author=cls.user)
        cls.comment = Comment.objects.create(
            text=TEST_TEXT_3,
            author=cls.user,
            post=cls.post)
        cls.EDIT_URLS = reverse(
            'edit_post',
            kwargs={'username': str(cls.user), 'post_id': cls.post.id})
        cls.COMMENT_URLS = reverse(
            'add_comment',
            kwargs={'username': cls.user, 'post_id': cls.post.id})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.authorixed_client = Client()
        self.authorixed_client.force_login(self.user)

    def test_create_new_post(self):
        """
        Проверка формы создания нового поста.
        """
        post_count = Post.objects.count()
        form_data = {
            'text': TEST_TEXT_2,
            'author': str(self.user),
            'image': UPLOADED}
        self.authorixed_client.post(
            NEW_POST_URLS,
            data=form_data)
        self.assertTrue(
            (Post.objects.count() == post_count + 1
             and Post.objects.filter(
                 text__exact=TEST_TEXT_2,
                 author__exact=self.user,
                 image__exact=URL_IMAGE).first()),
            MESS_COUNT_POST.format(post_count + 1))

    def test_edit_post(self):
        """
        Проверка формы редактирования поста.
        """
        primary_key = Post.objects.all()
        form_data = {'text': TEST_TEXT_2}
        self.authorixed_client.post(
            self.EDIT_URLS,
            data=form_data,
            follow=True)
        self.post.refresh_from_db()
        first_post = Post.objects.first()
        self.assertTrue(
            (first_post in primary_key
             and Post.objects.filter(
                 text__exact=TEST_TEXT_2,
                 author__exact=self.user).first()),
            MESS_EDIT_POST)

    def test_comment_edit(self):
        """
        Проверка формы создания комментария.
        """
        comment_count = Comment.objects.count()
        form_data = {'text': TEST_TEXT_3}
        self.authorixed_client.post(
            self.COMMENT_URLS,
            form_data,
            follow=True)
        self.post.refresh_from_db()
        self.assertTrue(
            (Comment.objects.count() == comment_count + 1
             and Comment.objects.filter(
                 text__exact=TEST_TEXT_3,
                 author__exact=self.user).first()),
            MESS_COUNT_COMMENT.format(comment_count + 1))
