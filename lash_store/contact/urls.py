from django.urls import path

from lash_store.contact.views import contact_page

urlpatterns = [
    path('',contact_page, name='contact-page'),
]