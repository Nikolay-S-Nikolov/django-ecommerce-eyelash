from django.urls import path

from lash_store.orders.views import cart_summary, add_to_cart_ajax, delete_cart_item

urlpatterns = [
    path ('cart/', cart_summary, name='cart_summary'),
    path('add_to_cart/<int:product_id>/', add_to_cart_ajax, name='add_to_cart'),
    path('cart/<int:pk>/', delete_cart_item, name='delete_cart_item'),
]