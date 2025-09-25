from django.urls import path

from lash_store.blog.views import blog_details_view, blog_list_view

urlpatterns = [
    path('', blog_list_view, name='blog_list'),
    path('<slug:slug>/', blog_details_view, name='blog_details'),
]