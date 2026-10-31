from django.db import models
from django.contrib.auth.models import User
from apps.catalog.models import Product, ProductVariant
from decimal import Decimal
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Guest Cart ({self.session_key})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def shipping_charge(self):
        # Can be configured via settings (e.g., Free over threshold or default 0)
        default_shipping = getattr(settings, 'STORE_DEFAULT_SHIPPING_FEE', 0)
        return Decimal(str(default_shipping))

    @property
    def total(self):
        return self.subtotal + self.shipping_charge

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        var_text = f" ({self.variant})" if self.variant else ""
        return f"{self.quantity}x {self.product.name}{var_text}"

    @property
    def unit_price(self):
        if self.variant and self.variant.price_override is not None:
            return self.variant.price_override
        return self.product.price

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    @property
    def available_stock(self):
        if self.variant:
            return self.variant.stock
        return self.product.stock

    @property
    def is_in_stock(self):
        return self.product.is_active and self.available_stock >= self.quantity
