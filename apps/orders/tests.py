from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product
from apps.cart.utils import get_or_create_cart
from apps.cart.models import CartItem
from .models import Order, OrderItem


class OrdersTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Footwear', slug='footwear')
        self.product = Product.objects.create(
            category=self.category,
            name='Nike Pegasus Running Shoes',
            slug='nike-pegasus',
            sku='NKE-PEG-01',
            price=Decimal('5000.00'),
            stock=10,
            is_active=True
        )

        self.user_a = User.objects.create_user(username='customer_a', email='a@example.com', password='Password@123')
        self.user_b = User.objects.create_user(username='customer_b', email='b@example.com', password='Password@123')

    def test_checkout_validation_and_order_creation(self):
        self.client.login(username='customer_a', password='Password@123')

        # Add 2 items to cart
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 2})

        # Submit valid checkout
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'Customer A',
            'email': 'a@example.com',
            'phone': '9876543210',
            'address_line1': '123 Park Street',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pin_code': '560001',
            'payment_method': 'cod',
        })

        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user_a).first()
        self.assertIsNotNone(order)
        self.assertTrue(order.order_number.startswith('BB-'))
        self.assertEqual(order.subtotal, Decimal('10000.00'))  # 2 * 5000
        self.assertEqual(order.total, Decimal('10000.00'))
        self.assertEqual(order.order_status, 'Confirmed')

        # Check stock deduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)  # 10 - 2

        # Check item snapshot
        order_item = order.items.first()
        self.assertEqual(order_item.product_name_snapshot, 'Nike Pegasus Running Shoes')
        self.assertEqual(order_item.unit_price_snapshot, Decimal('5000.00'))
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.line_total, Decimal('10000.00'))

    def test_user_cannot_access_another_users_order(self):
        # Create an order for User A
        order_a = Order.objects.create(
            user=self.user_a,
            full_name='User A',
            email='a@example.com',
            phone='9876543210',
            address_line1='Street A',
            city='Bengaluru',
            state='Karnataka',
            pin_code='560001',
            subtotal=Decimal('1000.00'),
            total=Decimal('1000.00'),
            payment_method='cod',
            order_status='Confirmed'
        )

        # Login as User B
        self.client.login(username='customer_b', password='Password@123')

        # Try to view User A's order detail -> Must return 404
        response = self.client.get(reverse('orders:order_detail', kwargs={'order_number': order_a.order_number}))
        self.assertEqual(response.status_code, 404)

        # User B's order history should not contain User A's order
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, order_a.order_number)

    def test_order_cancellation_restores_inventory(self):
        self.client.login(username='customer_a', password='Password@123')
        # Add 3 items to cart
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}), {'quantity': 3})

        # Checkout
        self.client.post(reverse('orders:checkout'), {
            'full_name': 'Customer A',
            'email': 'a@example.com',
            'phone': '9876543210',
            'address_line1': '123 Park Street',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pin_code': '560001',
            'payment_method': 'cod',
        })

        order = Order.objects.filter(user=self.user_a).first()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)  # 10 - 3

        # Cancel the order
        response = self.client.post(reverse('orders:cancel_order', kwargs={'order_number': order.order_number}))
        self.assertEqual(response.status_code, 302)

        order.refresh_from_db()
        self.assertEqual(order.order_status, 'Cancelled')

        # Stock must be restored to 10
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)
