from django.urls import path
from . import views
from .views import IndexView

urlpatterns = [
    # path("", views.home, name="home"),
    path("", IndexView.as_view(), name="home"),

]
