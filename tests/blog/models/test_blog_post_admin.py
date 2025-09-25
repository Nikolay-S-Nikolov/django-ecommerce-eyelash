from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from lash_store.blog.models import BlogPost
from lash_store.blog.admin import BlogPostAdmin

UserModel = get_user_model()

class BlogPostAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            email='admin@example.com',
            password='not_password'
        )
        self.admin = BlogPostAdmin(model=BlogPost, admin_site=None)

    def test_save_model_sets_author_on_create(self):
        request = self.factory.post('/admin/blogpost/add/')
        request.user = self.user

        post = BlogPost(title='Тестов пост', content='Съдържание')
        form = None
        change = False

        self.admin.save_model(request, post, form, change)

        self.assertEqual(post.author, self.user)
