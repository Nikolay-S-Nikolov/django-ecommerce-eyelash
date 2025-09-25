from django.shortcuts import render
from django.views import generic as views

from lash_store.blog.models import BlogPost


class BlogListView(views.ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)

blog_list_view = BlogListView.as_view()

class BlogDetailView(views.DetailView):
    model = BlogPost
    template_name = 'blog/blog_details.html'
    context_object_name = 'post'

blog_details_view = BlogDetailView.as_view()

