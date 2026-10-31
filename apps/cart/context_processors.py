from apps.cart.utils import get_or_create_cart


def cart_summary(request):
    """
    Context processor providing the current cart item count and summary
    to header navigation across the entire site.
    """
    try:
        cart = get_or_create_cart(request)
        return {
            'cart': cart,
            'cart_items_count': cart.total_items,
            'cart_total': cart.total,
        }
    except Exception:
        return {
            'cart': None,
            'cart_items_count': 0,
            'cart_total': 0,
        }
