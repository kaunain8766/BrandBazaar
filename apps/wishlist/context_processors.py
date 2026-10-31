from apps.wishlist.utils import get_or_create_wishlist


def wishlist_summary(request):
    """
    Context processor providing the wishlist count to header navigation.
    """
    try:
        wishlist = get_or_create_wishlist(request)
        return {
            'wishlist_items_count': wishlist.total_items,
        }
    except Exception:
        return {
            'wishlist_items_count': 0,
        }
