from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from django.db.models import Count

from lash_store.product.models import Product, ProductImages


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1  # колко празни реда за нови снимки да има по подразбиране
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:80px;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Preview"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]

    list_display = (
        'name', 
        'price', 
        'stock', 
        'units_sold',
        'image_count',
        'slug',
        'created_at', 
        'user',
        'updated_at',
        )
    search_fields = (
        'name', 
        'description',
        'slug',
        )
    list_filter = ('created_at', 'updated_at')
    fieldsets = (
        ('Основна информация', {
           'fields': ('name', 'price', 'stock', 'units_sold', 'user','slug' )
        }),
        ('Описание', {
            'fields': ('description', ) 
        }),
    )
    ordering = ('stock','-created_at','price', )
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', )
    prepopulated_fields = {'slug': ('name',)}



    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def image_count(self, obj):
        return obj.images.count()

    image_count.short_description = 'Брой снимки'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_images_count=Count('images'))

    image_count.admin_order_field = '_images_count'