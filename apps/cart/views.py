from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.catalog.models import Product, ProductVariant
from .models import CartItem
from .utils import get_or_create_cart


def cart_detail(request):
    """
    Renders shopping cart with all items, quantity controls,
    and server-recalculated subtotals and shipping.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'variant', 'product__brand').all()

    # Verify stock availability for all items in cart
    has_out_of_stock = False
    for item in cart_items:
        if not item.is_in_stock:
            has_out_of_stock = True

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'has_out_of_stock': has_out_of_stock,
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """
    Adds a product (and optional variant) to the cart with stock verification.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)

    # Quantity requested
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    # Check for variant selection
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        try:
            variant = ProductVariant.objects.get(id=variant_id, product=product, is_active=True)
        except ProductVariant.DoesNotExist:
            variant = None

    # Available stock
    available_stock = variant.stock if variant else product.stock

    if available_stock <= 0:
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect(product.get_absolute_url())

    # Check existing cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={'quantity': 0}
    )

    requested_total = cart_item.quantity + quantity
    if requested_total > available_stock:
        messages.warning(
            request,
            f"You requested {requested_total} units, but only {available_stock} are available. Added maximum available."
        )
        cart_item.quantity = available_stock
    else:
        cart_item.quantity = requested_total

    cart_item.save()
    messages.success(request, f"Added '{product.name}' to your cart.")

    # Redirect to cart or stay on product page based on 'action'
    if request.POST.get('buy_now') == '1':
        return redirect('orders:checkout')
    return redirect('cart:cart_detail')


@require_POST
def update_cart_item(request, item_id):
    """
    Updates the quantity of a specific cart item, ensuring it doesn't exceed stock.
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        new_quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        new_quantity = 1

    if new_quantity <= 0:
        cart_item.delete()
        messages.info(request, f"Removed '{cart_item.product.name}' from your cart.")
    else:
        max_stock = cart_item.available_stock
        if new_quantity > max_stock:
            cart_item.quantity = max_stock
            cart_item.save()
            messages.warning(request, f"Only {max_stock} units available for '{cart_item.product.name}'. Quantity adjusted.")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Cart quantity updated.")

    return redirect('cart:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
    """
    Removes an item completely from the cart.
    """
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f"Removed '{product_name}' from your cart.")
    return redirect('cart:cart_detail')


@require_POST
def clear_cart(request):
    """
    Empties the shopping cart.
    """
    cart = get_or_create_cart(request)
    cart.clear()
    messages.info(request, "Your shopping cart has been cleared.")
    return redirect('cart:cart_detail')
