from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product_name_snapshot', 'selected_variant_snapshot', 'unit_price_snapshot', 'quantity', 'line_total')
    readonly_fields = ('product_name_snapshot', 'selected_variant_snapshot', 'unit_price_snapshot', 'quantity', 'line_total')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'full_name',
        'email',
        'phone',
        'total',
        'payment_method',
        'payment_status',
        'order_status',
        'created_at'
    )
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'city', 'pin_code')
    list_editable = ('order_status', 'payment_status')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'shipping_charge', 'total')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name_snapshot', 'unit_price_snapshot', 'quantity', 'line_total')
    search_fields = ('order__order_number', 'product_name_snapshot')
