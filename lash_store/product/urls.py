from django.urls import path
from lash_store.product.views import ListProductView, DetailProductView

urlpatterns = [
    path ('', ListProductView.as_view(), name='products'),
    path('<slug:slug>/',DetailProductView.as_view() , name='product_details')
]