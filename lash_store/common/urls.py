from django.urls import path
from lash_store.common.views import about_view, index_view

urlpatterns = [
    path("", index_view, name="home"),
    path("about/", about_view, name="about"),
]