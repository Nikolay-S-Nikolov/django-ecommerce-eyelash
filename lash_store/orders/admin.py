from django.contrib import admin

from lash_store.orders.models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'saved_price')
    can_delete = False

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ('name', 'phone_number', 'email', 'address', 'city', 'postal_code', 'payment_method')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'status',
        'payment_status',
        'total_price',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'payment_status',
        'created_at',
    )

    search_fields = (
        'customer__username',
        'customer__email',
        'id',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'calculated_total_price',
    )

    fieldsets = (
        ('Информация за поръчката', {'fields': ('status', 'customer', 'total_price','payment_status', 'note')}),
        ('Дати', {'fields': ('created_at', 'updated_at')}),
    )

    inlines = [OrderItemInline, ShippingAddressInline]
    ordering = ('-created_at',)


