from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Brand, Product, ProductReview


def category_list(request):
    """List of all main top-level product categories."""
    categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children')
    return render(request, 'catalog/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """
    Displays products belonging to a category or any of its subcategories.
    Supports filtering by brand, price range, stock status, and multiple sort orders.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    descendant_ids = category.get_all_descendant_ids()

    products = Product.objects.filter(
        category_id__in=descendant_ids,
        is_active=True
    ).select_related('brand', 'category')

    # Brand filter
    selected_brand = request.GET.get('brand', '')
    if selected_brand:
        products = products.filter(brand__slug=selected_brand)

    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Availability filter
    in_stock = request.GET.get('in_stock', '')
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'bestseller':
        products = products.order_by('-is_bestseller', '-created_at')
    else:  # newest
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Brands available within this category tree for filter options
    available_brands = Brand.objects.filter(
        products__category_id__in=descendant_ids,
        is_active=True
    ).distinct().order_by('name')

    subcategories = category.children.filter(is_active=True)

    context = {
        'category': category,
        'products': page_obj,
        'total_count': products.count(),
        'available_brands': available_brands,
        'subcategories': subcategories,
        'selected_brand': selected_brand,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort': sort,
    }
    return render(request, 'catalog/category_detail.html', context)


def brand_list(request):
    """Displays all available brands with their product counts."""
    brands = Brand.objects.filter(is_active=True).order_by('name')
    return render(request, 'catalog/brand_list.html', {'brands': brands})


def brand_detail(request, slug):
    """Displays all products belonging to a specific brand."""
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True).select_related('category')

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 9)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, 'catalog/brand_detail.html', {
        'brand': brand,
        'products': page_obj,
        'sort': sort,
        'total_count': products.count()
    })


def product_list(request):
    """Global all-products listing with full filtering & sorting."""
    products = Product.objects.filter(is_active=True).select_related('brand', 'category')

    # Category filter
    selected_category = request.GET.get('category', '')
    if selected_category:
        cat = Category.objects.filter(slug=selected_category, is_active=True).first()
        if cat:
            products = products.filter(category_id__in=cat.get_all_descendant_ids())

    # Brand filter
    selected_brand = request.GET.get('brand', '')
    if selected_brand:
        products = products.filter(brand__slug=selected_brand)

    # Price filters
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    in_stock = request.GET.get('in_stock', '')
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    categories = Category.objects.filter(parent__isnull=True, is_active=True)
    brands = Brand.objects.filter(is_active=True)

    context = {
        'products': page_obj,
        'total_count': products.count(),
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort': sort,
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    """
    Detailed product view showing images, variants, stock, description,
    customer reviews, and related recommendations.
    """
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category').prefetch_related('gallery_images', 'variants', 'reviews__user'),
        slug=slug,
        is_active=True
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    if not related_products.exists() and product.brand:
        related_products = Product.objects.filter(
            brand=product.brand,
            is_active=True
        ).exclude(id=product.id)[:4]

    reviews = product.reviews.filter(is_approved=True)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'catalog/product_detail.html', context)


def search(request):
    """
    Comprehensive search across products, brands, categories, and descriptions.
    """
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).select_related('brand', 'category').distinct()

        sort = request.GET.get('sort', 'relevance')
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'name_asc':
            products = products.order_by('name')
        elif sort == 'newest':
            products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    context = {
        'search_query': query,
        'products': page_obj,
        'total_count': products.count(),
        'sort': request.GET.get('sort', ''),
    }
    return render(request, 'catalog/search_results.html', context)


@login_required
def add_review(request, slug):
    """Handles submission of user product reviews."""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        headline = request.POST.get('headline', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not rating or not headline or not comment:
            messages.error(request, "Please fill in all review fields and select a star rating.")
        else:
            try:
                rating_int = int(rating)
                if not 1 <= rating_int <= 5:
                    raise ValueError()

                ProductReview.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={
                        'rating': rating_int,
                        'headline': headline,
                        'comment': comment,
                        'is_approved': True
                    }
                )
                messages.success(request, "Thank you! Your product review has been submitted.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid rating submitted.")

    return redirect('catalog:product_detail', slug=slug)
