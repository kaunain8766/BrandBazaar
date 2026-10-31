import os
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from apps.catalog.models import Category, Brand, Product, ProductImage, ProductVariant, ProductReview
from apps.accounts.models import UserProfile
from generate_media_assets import BRAND_LOGOS, CATEGORY_VISUALS, make_product_svg, PRODUCT_CONFIGS


class Command(BaseCommand):
    help = 'Populates the database with realistic demo categories, brands, products, variants, reviews, and high-fidelity media assets.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing BrandBazaar Demo Data & Media Assets..."))

        # 1. Create Default Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@brandbazaar.com',
                'first_name': 'Store',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin@12345')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: admin (password: Admin@12345)"))

        demo_customer, created = User.objects.get_or_create(
            username='customer',
            defaults={
                'email': 'customer@brandbazaar.com',
                'first_name': 'Aarav',
                'last_name': 'Sharma',
            }
        )
        if created:
            demo_customer.set_password('Customer@12345')
            demo_customer.save()
            demo_profile, _ = UserProfile.objects.get_or_create(user=demo_customer)
            demo_profile.phone = '+91 98765 43210'
            demo_profile.address_line1 = 'Flat 402, Lotus Residency, MG Road'
            demo_profile.city = 'Bengaluru'
            demo_profile.state = 'Karnataka'
            demo_profile.pin_code = '560001'
            demo_profile.save()
            self.stdout.write(self.style.SUCCESS("Created demo customer: customer (password: Customer@12345)"))

        # 2. Brands & Vector Logos
        brands_data = [
            ("Levi's", "levis", "Iconic denim & American casual wear since 1853", True),
            ("Nike", "nike", "World leader in athletic footwear, apparel and equipment", True),
            ("Puma", "puma", "Forever Faster sportswear, training shoes and lifestyle gear", True),
            ("Sony", "sony", "Premium audio equipment, noise-canceling headphones & tech", True),
            ("boAt", "boat", "India's top audio and smart wearable lifestyle brand", True),
            ("Samsung", "samsung", "Cutting-edge mobile devices, wearables and electronics", True),
            ("Zara", "zara", "Contemporary global high-street fashion and everyday style", True),
            ("Allen Solly", "allen-solly", "Sophisticated Friday dressing, formal wear and casual shirts", True),
            ("L'Oréal Paris", "loreal-paris", "World-renowned French beauty, haircare and skincare", True),
            ("Maybelline", "maybelline", "New York urban makeup, cosmetics and beauty essentials", True),
        ]

        brand_objs = {}
        for name, slug, desc, featured in brands_data:
            brand, _ = Brand.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': desc,
                    'is_featured': featured,
                    'is_active': True,
                }
            )
            if slug in BRAND_LOGOS:
                brand.logo.save(f"{slug}-logo.svg", ContentFile(BRAND_LOGOS[slug].encode('utf-8')), save=True)
            brand_objs[slug] = brand
        self.stdout.write(self.style.SUCCESS(f"Configured {len(brand_objs)} Brands with authentic vector logos."))

        # 3. Categories & Visuals
        clothes, _ = Category.objects.get_or_create(
            slug='clothes',
            defaults={'name': 'Clothes', 'description': 'Trendy, comfortable, and premium clothing for all occasions.', 'order': 1}
        )
        if 'clothes' in CATEGORY_VISUALS:
            clothes.image.save('clothes.svg', ContentFile(CATEGORY_VISUALS['clothes'].encode('utf-8')), save=True)

        cat_men, _ = Category.objects.get_or_create(slug='men', parent=clothes, defaults={'name': 'Men', 'order': 1})
        cat_women, _ = Category.objects.get_or_create(slug='women', parent=clothes, defaults={'name': 'Women', 'order': 2})
        cat_kids, _ = Category.objects.get_or_create(slug='kids', parent=clothes, defaults={'name': 'Kids', 'order': 3})

        subcats = {}
        for name, slug in [('Shirts', 'men-shirts'), ('T-Shirts', 'men-t-shirts'), ('Jeans', 'men-jeans'), 
                           ('Jackets', 'men-jackets'), ('Hoodies', 'men-hoodies'), ('Shorts', 'men-shorts'), ('Accessories', 'men-accessories')]:
            sc, _ = Category.objects.get_or_create(slug=slug, parent=cat_men, defaults={'name': name})
            subcats[slug] = sc

        for name, slug in [('Dresses', 'women-dresses'), ('Tops', 'women-tops'), ('Jeans', 'women-jeans'),
                           ('Shirts', 'women-shirts'), ('Jackets', 'women-jackets'), ('Accessories', 'women-accessories')]:
            sc, _ = Category.objects.get_or_create(slug=slug, parent=cat_women, defaults={'name': name})
            subcats[slug] = sc

        for name, slug in [('T-Shirts', 'kids-t-shirts'), ('Shirts', 'kids-shirts'), ('Jeans', 'kids-jeans'),
                           ('Dresses', 'kids-dresses'), ('Accessories', 'kids-accessories')]:
            sc, _ = Category.objects.get_or_create(slug=slug, parent=cat_kids, defaults={'name': name})
            subcats[slug] = sc

        footwear, _ = Category.objects.get_or_create(
            slug='footwear',
            defaults={'name': 'Footwear', 'description': 'Sneakers, sports shoes, formal shoes and casual sandals.', 'order': 2}
        )
        if 'footwear' in CATEGORY_VISUALS:
            footwear.image.save('footwear.svg', ContentFile(CATEGORY_VISUALS['footwear'].encode('utf-8')), save=True)

        cat_fw_men, _ = Category.objects.get_or_create(slug='mens-footwear', parent=footwear, defaults={'name': "Men's Footwear", 'order': 1})
        cat_fw_women, _ = Category.objects.get_or_create(slug='womens-footwear', parent=footwear, defaults={'name': "Women's Footwear", 'order': 2})

        subcats['mens-sneakers'], _ = Category.objects.get_or_create(slug='mens-sneakers', parent=cat_fw_men, defaults={'name': 'Sneakers'})
        subcats['mens-running'], _ = Category.objects.get_or_create(slug='mens-running', parent=cat_fw_men, defaults={'name': 'Running Shoes'})
        subcats['mens-formal'], _ = Category.objects.get_or_create(slug='mens-formal', parent=cat_fw_men, defaults={'name': 'Formal Shoes'})
        subcats['womens-sneakers'], _ = Category.objects.get_or_create(slug='womens-sneakers', parent=cat_fw_women, defaults={'name': 'Sneakers'})
        subcats['womens-heels'], _ = Category.objects.get_or_create(slug='womens-heels', parent=cat_fw_women, defaults={'name': 'Heels & Flats'})

        beauty, _ = Category.objects.get_or_create(
            slug='beauty-personal-care',
            defaults={'name': 'Beauty & Personal Care', 'description': 'Premium skincare, haircare, makeup, and luxury fragrances.', 'order': 3}
        )
        if 'beauty' in CATEGORY_VISUALS:
            beauty.image.save('beauty.svg', ContentFile(CATEGORY_VISUALS['beauty'].encode('utf-8')), save=True)

        subcats['skincare'], _ = Category.objects.get_or_create(slug='skincare', parent=beauty, defaults={'name': 'Skincare'})
        subcats['haircare'], _ = Category.objects.get_or_create(slug='haircare', parent=beauty, defaults={'name': 'Haircare'})
        subcats['makeup'], _ = Category.objects.get_or_create(slug='makeup', parent=beauty, defaults={'name': 'Makeup'})
        subcats['fragrance'], _ = Category.objects.get_or_create(slug='fragrance', parent=beauty, defaults={'name': 'Fragrances'})

        electronics, _ = Category.objects.get_or_create(
            slug='electronics',
            defaults={'name': 'Electronics', 'description': 'High-performance audio, smart watches, wearables & accessories.', 'order': 4}
        )
        if 'electronics' in CATEGORY_VISUALS:
            electronics.image.save('electronics.svg', ContentFile(CATEGORY_VISUALS['electronics'].encode('utf-8')), save=True)

        subcats['audio'], _ = Category.objects.get_or_create(slug='audio-headphones', parent=electronics, defaults={'name': 'Audio & Headphones'})
        subcats['smartwatches'], _ = Category.objects.get_or_create(slug='smartwatches', parent=electronics, defaults={'name': 'Smartwatches & Wearables'})
        subcats['accessories-electronics'], _ = Category.objects.get_or_create(slug='mobile-accessories', parent=electronics, defaults={'name': 'Mobile Accessories'})

        self.stdout.write(self.style.SUCCESS("Categories and hierarchy configured with custom graphics."))
        self.stdout.write(self.style.SUCCESS("Media assets ready!"))
