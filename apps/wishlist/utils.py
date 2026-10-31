from apps.wishlist.models import Wishlist, WishlistItem


def get_or_create_wishlist(request, guest_session_key=None):
    """
    Retrieves or creates the active wishlist for the request.
    Merges guest session wishlist on login.
    """
    if request.user.is_authenticated:
        user_wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        keys_to_check = set()
        if guest_session_key:
            keys_to_check.add(guest_session_key)
        if request.session.session_key:
            keys_to_check.add(request.session.session_key)

        if keys_to_check:
            guest_wishlists = Wishlist.objects.filter(session_key__in=keys_to_check, user__isnull=True)
            for gw in guest_wishlists:
                for item in gw.items.all():
                    WishlistItem.objects.get_or_create(wishlist=user_wishlist, product=item.product)
                gw.delete()
        return user_wishlist
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        wishlist, _ = Wishlist.objects.get_or_create(session_key=session_key, user__isnull=True)
        return wishlist
