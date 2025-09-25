from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from lash_store.blog.models import BlogPost
from lash_store.blog.views import BlogListView

UserModel = get_user_model()

class BlogListViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='not_password'
        )
        self.post_published = BlogPost.objects.create(
            title='Публикуван пост',
            content='Съдържание',
            author=self.user,
            published=True
        )

        self.post_unpublished = BlogPost.objects.create(
            title='Чернова',
            content='Скрита чернова',
            author=self.user,
            published=False
        )

    def test__only_published_posts_are_displayed(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')
        self.assertContains(response, self.post_published.title)
        self.assertNotContains(response, self.post_unpublished.title)

    def test__queryset_filters_unpublished(self):
        view = BlogListView()
        view.request = self.client.request().wsgi_request
        queryset = view.get_queryset()
        self.assertIn(self.post_published, queryset)
        self.assertNotIn(self.post_unpublished, queryset)
