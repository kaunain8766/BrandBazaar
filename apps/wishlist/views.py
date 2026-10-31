from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.catalog.models import Product
from apps.cart.utils import get_or_create_cart
from apps.cart.models import CartItem
from .models import WishlistItem
from .utils import get_or_create_wishlist


def wishlist_detail(request):
    """
    Displays the user's wishlist products with options to move to cart or remove.
    """
    wishlist = get_or_create_wishlist(request)
    items = wishlist.items.select_related('product', 'product__brand').all()
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist': wishlist, 'items': items})


@require_POST
def toggle_wishlist(request, product_id):
    """
    Toggles a product in the wishlist (adds if absent, removes if present).
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)

    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if item:
        item.delete()
        messages.info(request, f"Removed '{product.name}' from your wishlist.")
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"Added '{product.name}' to your wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist_detail'))


@require_POST
def remove_from_wishlist(request, product_id):
    """
    Removes a product from the wishlist.
    """
    wishlist = get_or_create_wishlist(request)
    WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id).delete()
    messages.info(request, "Item removed from your wishlist.")
    return redirect('wishlist:wishlist_detail')


@require_POST
def move_to_cart(request, product_id):
    """
    Moves an item from wishlist to cart and removes it from wishlist.
    """
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist = get_or_create_wishlist(request)
    cart = get_or_create_cart(request)

    if product.stock <= 0:
        messages.warning(request, f"'{product.name}' is currently out of stock.")
        return redirect('wishlist:wishlist_detail')

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    # Remove from wishlist
    WishlistItem.objects.filter(wishlist=wishlist, product=product).delete()
    messages.success(request, f"Moved '{product.name}' to your cart.")
    return redirect('cart:cart_detail')
