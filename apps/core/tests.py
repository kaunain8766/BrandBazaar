from django.test import TestCase
from django.urls import reverse
from apps.catalog.models import Category, Product


class CoreViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Clothes', slug='clothes')
        self.product = Product.objects.create(
            category=self.category,
            name='Test T-Shirt',
            slug='test-t-shirt',
            sku='TEST-001',
            price=499.00,
            stock=10,
            is_active=True,
            is_trending=True,
            is_bestseller=True
        )

    def test_home_page_status_code_and_content(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, 'BrandBazaar')
        self.assertContains(response, 'Test T-Shirt')

    def test_informational_pages(self):
        urls = [
            'core:about',
            'core:contact',
            'core:faq',
            'core:shipping_policy',
            'core:return_policy',
            'core:privacy_policy',
            'core:terms',
        ]
        for url_name in urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_newsletter_subscription(self):
        response = self.client.post(reverse('core:newsletter_subscribe'), {'email': 'shopper@example.com'})
        self.assertEqual(response.status_code, 302)

    def test_contact_form_submission(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Rohan Das',
            'email': 'rohan@example.com',
            'subject': 'Sizing question',
            'message': 'Need assistance with Levi jeans sizes.'
        })
        self.assertEqual(response.status_code, 302)
