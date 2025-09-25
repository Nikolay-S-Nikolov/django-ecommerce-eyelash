from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from slugify import slugify

from lash_store.blog.models import BlogPost

UserModel = get_user_model()

class BlogPostModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='not_password'
        )

    def test__slug_is_generated_on_save(self):
        post = BlogPost.objects.create(
            title='Тестов пост',
            content='Това е съдържание на тестов пост.',
            author=self.user
        )
        expected_slug = slugify(post.title)
        self.assertEqual(post.slug, expected_slug)

    def test__slug_is_unique_when_titles_repeat(self):
        title = 'Повтарящо се заглавие'
        post1 = BlogPost.objects.create(
            title=title,
            content='Първо съдържание',
            author=self.user
        )
        post2 = BlogPost.objects.create(
            title=title,
            content='Второ съдържание',
            author=self.user
        )
        self.assertNotEqual(post1.slug, post2.slug)
        self.assertTrue(post2.slug.startswith(slugify(title)))
        self.assertIn('-', post2.slug)

    def test__create_excerpt_method_sets_excerpt(self):
        post = BlogPost.objects.create(
            title='Заглавие',
            content='Това е много дълго съдържание ' * 200,
            author=self.user
        )
        post.create_excerpt()
        self.assertIsNotNone(post.excerpt)
        self.assertLessEqual(len(post.excerpt), 250)

    def test__str_method_returns_correct_format(self):
        post = BlogPost.objects.create(
            title='Заглавие',
            content='Съдържание',
            author=self.user
        )
        expected_str = f'{post.title} ({post.created_at.strftime("%d.%m.%Y")})'
        self.assertEqual(str(post), expected_str)