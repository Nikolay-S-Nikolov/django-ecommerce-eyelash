from django.views import generic as views
from lash_store.product.models import Product


class ListProductView(views.ListView):
    model = Product
    template_name = 'product/product_list.html'
    paginate_by = 6
    ordering = ['-created_at']

class DetailProductView(views.DetailView):
    model = Product
    template_name = 'product/product_detail.html'