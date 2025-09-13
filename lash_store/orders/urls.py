from django.urls import path
from lash_store.orders.views import cart_summary, add_to_cart_ajax, delete_cart_item, update_cart_item_quantity_ajax, \
    checkout_view, order_confirmation_view, orders_history_view

urlpatterns = [
    path('', checkout_view, name='checkout'),
    path('confirmation/<int:pk>/', order_confirmation_view, name='order_confirmation'),
    path ('cart/', cart_summary, name='cart_summary'),
    path('add_to_cart/<int:product_id>/', add_to_cart_ajax, name='add_to_cart'),
    path('cart/<int:pk>/delete/', delete_cart_item, name='delete_cart_item'),
    path('cart/<int:cart_item_id>/update/', update_cart_item_quantity_ajax, name='update_cart_item'),
    path('orders/', orders_history_view, name='orders_history'),
]