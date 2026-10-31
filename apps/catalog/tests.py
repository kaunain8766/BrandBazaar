from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Brand, Product, ProductVariant, ProductReview


class CatalogTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="Levi's", slug="levis", is_active=True, is_featured=True)
        self.parent_cat = Category.objects.create(name='Clothes', slug='clothes', is_active=True)
        self.sub_cat = Category.objects.create(name='Men', slug='men', parent=self.parent_cat, is_active=True)
        self.leaf_cat = Category.objects.create(name='Jeans', slug='men-jeans', parent=self.sub_cat, is_active=True)

        self.p1 = Product.objects.create(
            name="Levi's 511 Slim Fit Jeans",
            slug='levis-511-slim-fit-jeans',
            sku='LEV-511-01',
            brand=self.brand,
            category=self.leaf_cat,
            price=Decimal('2500.00'),
            original_price=Decimal('3500.00'),
            stock=15,
            is_active=True
        )

        self.p2 = Product.objects.create(
            name="Puma White Sneakers",
            slug='puma-white-sneakers',
            sku='PUM-01',
            category=self.parent_cat,
            price=Decimal('1800.00'),
            stock=5,
            is_active=True
        )

        self.user = User.objects.create_user(username='tester', password='Password@123')

    def test_category_detail_loads_and_includes_subcategories(self):
        # Browsing top parent 'Clothes' should find product in grandchild 'Jeans'
        response = self.client.get(reverse('catalog:category_detail', kwargs={'slug': 'clothes'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "511 Slim Fit Jeans")
        self.assertContains(response, "Puma White Sneakers")

    def test_product_detail_page(self):
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': self.p1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "511 Slim Fit Jeans")
        self.assertContains(response, "2500.00")

    def test_search_functionality(self):
        response = self.client.get(reverse('catalog:search'), {'q': 'Slim Fit'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "511 Slim Fit Jeans")
        self.assertNotContains(response, "Puma White Sneakers")

    def test_filtering_by_brand(self):
        response = self.client.get(reverse('catalog:category_detail', kwargs={'slug': 'clothes'}), {'brand': 'levis'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "511 Slim Fit Jeans")
        self.assertNotContains(response, "Puma White Sneakers")

    def test_sorting_by_price_asc(self):
        response = self.client.get(reverse('catalog:product_list'), {'sort': 'price_asc'})
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0], self.p2)  # 1800 < 2500

    def test_add_review_authenticated(self):
        self.client.login(username='tester', password='Password@123')
        response = self.client.post(reverse('catalog:add_review', kwargs={'slug': self.p1.slug}), {
            'rating': '5',
            'headline': 'Super comfortable',
            'comment': 'Best denim purchase this year.'
        })
        self.assertEqual(response.status_code, 302)
        review = ProductReview.objects.get(product=self.p1, user=self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.headline, 'Super comfortable')
