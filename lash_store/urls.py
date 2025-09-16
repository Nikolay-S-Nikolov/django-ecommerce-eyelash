"""
URL configuration for lash_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from lash_store.settings import DEBUG

urlpatterns = [
    path("", include('lash_store.common.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("lash_store.accounts.url")),
    path("i18n/", include("django.conf.urls.i18n")),
    path('product/', include("lash_store.product.urls")),
    path('checkout/', include("lash_store.orders.urls")),

]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)