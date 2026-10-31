from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product
from .models import Cart, CartItem


class CartTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='boAt Earbuds',
            slug='boat-earbuds',
            sku='BOAT-01',
            price=Decimal('1299.00'),
            stock=5,
            is_active=True
        )

    def test_guest_add_to_cart(self):
        response = self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {
            'quantity': 2
        })
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        self.assertEqual(cart.total_items, 2)
        self.assertEqual(cart.subtotal, Decimal('2598.00'))

    def test_cart_quantity_cannot_exceed_stock(self):
        # Stock is 5, attempt to add 10
        response = self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {
            'quantity': 10
        })
        cart = Cart.objects.first()
        # Should cap at available stock (5)
        self.assertEqual(cart.total_items, 5)

    def test_cart_item_update_and_removal(self):
        # Add 1
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 1})
        cart = Cart.objects.first()
        item = cart.items.first()

        # Update to 3
        self.client.post(reverse('cart:update_cart_item', kwargs={'item_id': item.id}), {'quantity': 3})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

        # Remove
        self.client.post(reverse('cart:remove_from_cart', kwargs={'item_id': item.id}))
        self.assertEqual(cart.items.count(), 0)

    def test_cart_merges_on_login(self):
        # Guest adds product
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 2})
        guest_cart = Cart.objects.first()
        self.assertEqual(guest_cart.total_items, 2)

        # User logs in through the login POST view
        User.objects.create_user(username='buyer', password='Password@123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'buyer',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username='buyer')
        user_cart = Cart.objects.get(user=user)
        self.assertEqual(user_cart.total_items, 2)
