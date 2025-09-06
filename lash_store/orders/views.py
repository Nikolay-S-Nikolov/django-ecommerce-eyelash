from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic as views

from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product


class CartSummaryView(views.TemplateView):
    template_name = 'orders/cart.html'

cart_summary = CartSummaryView.as_view()

def add_to_cart_ajax(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += 1 #1 only for test TO BE REMOVED after test
        item.save()

        picture_url = product.images.first().image.url if product.images.exists() else ''

        return JsonResponse({
            "success": True,
            "message": "Продуктът е добавен в кошницата",
            "product_details": {
                "name": product.name,
                "price": str(product.price),
                "quantity": item.quantity,
                "picture": picture_url,
                "slug": product.slug,
            }
        })
    return JsonResponse({"success": False, "message": "Невалидна заявка"})