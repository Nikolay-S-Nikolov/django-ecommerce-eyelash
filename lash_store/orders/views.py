import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic as views

from lash_store.orders.models import Cart, CartItem
from lash_store.product.models import Product

class CartSummaryView(views.ListView):
    model = CartItem
    template_name = 'orders/cart.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.select_related('product').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['object_list']
        context['total'] = sum(item.product.price * item.quantity for item in cart_items)
        return context

cart_summary = CartSummaryView.as_view()

def add_to_cart_ajax(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        data = json.loads(request.body)
        quantity = int(data.get("quantity"))

        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        item.quantity += quantity -1 if created else quantity
        message = "Продуктът е добавен в кошницата"

        if item.quantity > item.product.stock:
            item.quantity = item.product.stock
            message = f"От този продукт може да купите максимум {item.product.stock} бр."


        item.save()

        picture_url = product.images.first().image.url if product.images.exists() else ''

        return JsonResponse({
            "success": True,
            "message": message,
            "product_details": {
                "name": product.name,
                "price": str(product.price),
                "quantity": item.quantity,
                "picture": picture_url,
                "slug": product.slug,
            }
        })
    return JsonResponse({"success": False, "message": "Невалидна заявка"})