from django.urls import path
from lash_store.common.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),

]