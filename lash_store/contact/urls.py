from django.urls import path

from lash_store.contact.views import contact_page, send_contact_message

urlpatterns = [
    path('',contact_page, name='contact-page'),
    path('contact/send/', send_contact_message, name='send_contact_message'),
]