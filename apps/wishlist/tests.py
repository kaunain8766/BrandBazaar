from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product
from .models import Wishlist, WishlistItem


class WishlistTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Footwear', slug='footwear')
        self.product = Product.objects.create(
            category=self.category,
            name='Nike Pegasus',
            slug='nike-pegasus',
            sku='NKE-01',
            price=8000.00,
            stock=10,
            is_active=True
        )

    def test_toggle_wishlist(self):
        # Toggle 1: Add
        response = self.client.post(reverse('wishlist:toggle_wishlist', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 302)
        wishlist = Wishlist.objects.first()
        self.assertEqual(wishlist.total_items, 1)

        # Toggle 2: Remove
        response = self.client.post(reverse('wishlist:toggle_wishlist', kwargs={'product_id': self.product.id}))
        self.assertEqual(wishlist.total_items, 0)

    def test_move_to_cart(self):
        # Add to wishlist
        self.client.post(reverse('wishlist:toggle_wishlist', kwargs={'product_id': self.product.id}))
        wishlist = Wishlist.objects.first()
        self.assertEqual(wishlist.total_items, 1)

        # Move to cart
        response = self.client.post(reverse('wishlist:move_to_cart', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(wishlist.total_items, 0)
