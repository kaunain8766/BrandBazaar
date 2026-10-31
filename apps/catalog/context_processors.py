from apps.catalog.models import Category, Brand
from django.conf import settings


def category_navigation(request):
    """
    Context processor to make top-level navigation categories
    and featured brands accessible across all templates.
    """
    top_categories = Category.objects.filter(
        parent__isnull=True,
        is_active=True
    ).prefetch_related(
        'children__children'
    ).order_by('order', 'name')

    featured_brands = Brand.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('name')[:8]

    return {
        'nav_categories': top_categories,
        'featured_brands_nav': featured_brands,
        'STORE_NAME': getattr(settings, 'STORE_NAME', 'BrandBazaar'),
        'CURRENCY_SYMBOL': getattr(settings, 'STORE_CURRENCY_SYMBOL', '₹'),
    }
