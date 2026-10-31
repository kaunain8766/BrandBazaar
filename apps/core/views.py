from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.catalog.models import Category, Brand, Product


def home(request):
    """
    Homepage featuring hero banner, category circles, featured brands,
    trending products, new arrivals, and bestsellers.
    """
    top_categories = Category.objects.filter(
        parent__isnull=True,
        is_active=True
    ).order_by('order', 'name')

    featured_brands = Brand.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('name')

    trending_products = Product.objects.filter(
        is_active=True,
        is_trending=True
    ).select_related('brand', 'category')[:8]

    new_arrivals = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').order_by('-created_at')[:8]

    bestsellers = Product.objects.filter(
        is_active=True,
        is_bestseller=True
    ).select_related('brand', 'category')[:8]

    context = {
        'top_categories': top_categories,
        'featured_brands': featured_brands,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'bestsellers': bestsellers,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                validate_email(email)
                messages.success(request, f"Thank you {name}! Your message has been received. Our team will contact you shortly.")
                return redirect('core:contact')
            except ValidationError:
                messages.error(request, "Please provide a valid email address.")

    return render(request, 'core/contact.html')


def faq(request):
    return render(request, 'core/faq.html')


def shipping_policy(request):
    return render(request, 'core/shipping_policy.html')


def return_policy(request):
    return render(request, 'core/return_policy.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def terms(request):
    return render(request, 'core/terms.html')


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            messages.error(request, "Please enter an email address.")
        else:
            try:
                validate_email(email)
                messages.success(request, "Thank you for subscribing to BrandBazaar updates!")
            except ValidationError:
                messages.error(request, "Please provide a valid email address.")
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))


def handler404(request, exception=None):
    return render(request, 'core/404.html', status=404)
