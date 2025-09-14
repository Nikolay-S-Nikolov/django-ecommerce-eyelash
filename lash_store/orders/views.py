import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from lash_store.orders.decorators import ajax_login_required
from lash_store.orders.forms import CheckoutForm
from lash_store.orders.models import Cart, CartItem, OrderItem, Order
from lash_store.product.models import Product


class CartSummaryView(LoginRequiredMixin,views.ListView):
    model = CartItem
    template_name = 'orders/cart.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.select_related('product').all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['object_list']
        context['total'] = sum(item.product.price * item.quantity for item in cart_items)
        return context

cart_summary = CartSummaryView.as_view()

@ajax_login_required
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


class DeleteCartItemView(LoginRequiredMixin,views.View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

        if self.request.user != cart_item.cart.user:
            raise PermissionDenied("You don't have permission to remove this cart item.")

        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"Продукта {product_name} е успешно премахнат от кошницата.")
        return HttpResponseRedirect(reverse('cart_summary'))

delete_cart_item = DeleteCartItemView.as_view()

@ajax_login_required
def update_cart_item_quantity_ajax(request, cart_item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        data = json.loads(request.body)
        quantity = int(data.get("quantity"))

        cart_item.quantity += quantity
        if cart_item.quantity == 0:
            cart_item.quantity=1
        message = "Количеството е обновено успешно"

        if cart_item.quantity > cart_item.product.stock:
            cart_item.quantity = cart_item.product.stock
            message = f"От този продукт може да купите максимум {cart_item.product.stock} бр."

        cart_item.save()

        return JsonResponse({
            "success": True,
            "message": message,
            "product_details": {
                "quantity": cart_item.quantity,
                "total_price": str(cart_item.product.price * cart_item.quantity),
                "cart_total": str(sum(item.product.price * item.quantity for item in cart_item.cart.items.all())),
            }
        })
    return JsonResponse({"success": False, "message": "Невалидна заявка"})


class CheckoutView(LoginRequiredMixin, views.FormView):
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm
    order_id = None

    def get_success_url(self):
        return reverse_lazy('order_confirmation', kwargs={'pk': self.order_id})

    def dispatch(self, request, *args, **kwargs):
        if not self.get_cart_items().exists():
            messages.warning(request, "Вашата количка е празна. Добавете продукти преди да завършите поръчката.")
            return redirect('cart_summary')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = self.calculate_total_price(cart_items)
        return context

    def form_valid(self, form):
        cart_items = self.get_cart_items()

        if not cart_items.exists():
            messages.error(self.request, "Вашата количка е празна. Добавете продукти преди да завършите поръчката.")
            return redirect('cart_summary')

        order = form.save()
        self.order_id = order.id

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                saved_price=cart_item.product.price*cart_item.quantity,
            ) for cart_item in cart_items
        ])

        for item in cart_items:
            item.product.units_sold += item.quantity
            item.product.save()

        cart_items.delete()

        messages.success(self.request, "Поръчката е изпратена за обработка!")
        return super().form_valid(form)

    @staticmethod
    def calculate_total_price(items):
        total_price = sum(item.product.price * item.quantity for item in items)
        return total_price

    def get_cart_items(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related('product').all()

checkout_view = CheckoutView.as_view()

class OrderConfirmationView(LoginRequiredMixin, views.DetailView):
    model = Order
    template_name = 'orders/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

order_confirmation_view = OrderConfirmationView.as_view()

class OrderHistoryView(LoginRequiredMixin, views.ListView):
    model = Order
    template_name = 'orders/orders_history.html'
    context_object_name = 'orders'
    # paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')

orders_history_view = OrderHistoryView.as_view()

class OrderDetailView(LoginRequiredMixin, views.DetailView):
    model = Order
    template_name = 'orders/order_details.html'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

order_detail_view = OrderDetailView.as_view()