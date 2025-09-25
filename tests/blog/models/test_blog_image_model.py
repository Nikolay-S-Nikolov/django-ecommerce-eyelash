from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from lash_store.blog.models import BlogPost, BlogImage

UserModel = get_user_model()

class BlogImageModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='not_password'
        )
        self.post = BlogPost.objects.create(
            title='Тестов пост',
            content='Съдържание на поста',
            author=self.user
        )
        self.test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )

    def test__blog_image_creation(self):
        image = BlogImage.objects.create(
            post=self.post,
            image=self.test_image,
            alt_text='Тестово изображение'
        )
        self.assertEqual(image.post, self.post)
        self.assertEqual(image.alt_text, 'Тестово изображение')
        self.assertTrue(image.image.url.startswith('/media/blog_images/test'))

    def test__blog_image_str_method(self):
        image = BlogImage.objects.create(
            post=self.post,
            image=self.test_image,
            alt_text='Описание'
        )
        expected_str = f'Изображение за пост: {self.post.title}'
        self.assertEqual(str(image), expected_str)

    def test__alt_text_can_be_blank(self):
        image = BlogImage.objects.create(
            post=self.post,
            image=self.test_image,
            alt_text=''
        )
        self.assertEqual(image.alt_text, '')

    def test__alt_text_max_length(self):
        long_text = 'а' * BlogImage.MAX_CAPTION_LENGTH
        image = BlogImage.objects.create(
            post=self.post,
            image=self.test_image,
            alt_text=long_text
        )
        self.assertEqual(len(image.alt_text), BlogImage.MAX_CAPTION_LENGTH)
