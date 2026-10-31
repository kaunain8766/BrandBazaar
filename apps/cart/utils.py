from apps.cart.models import Cart, CartItem


def get_or_create_cart(request, guest_session_key=None):
    """
    Retrieves or creates the active cart for the request.
    Handles seamless merging of guest session cart when a user logs in.
    """
    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)

        # Check guest session keys to merge (both pre-login and current)
        keys_to_check = set()
        if guest_session_key:
            keys_to_check.add(guest_session_key)
        if request.session.session_key:
            keys_to_check.add(request.session.session_key)

        # Also merge any carts with user__isnull=True that might have belonged to this session
        if keys_to_check:
            guest_carts = Cart.objects.filter(session_key__in=keys_to_check, user__isnull=True)
            for guest_cart in guest_carts:
                for item in guest_cart.items.all():
                    existing_item = CartItem.objects.filter(
                        cart=user_cart,
                        product=item.product,
                        variant=item.variant
                    ).first()

                    if existing_item:
                        max_stock = existing_item.available_stock
                        new_qty = min(existing_item.quantity + item.quantity, max_stock)
                        existing_item.quantity = new_qty
                        existing_item.save()
                        item.delete()
                    else:
                        item.cart = user_cart
                        item.save()
                guest_cart.delete()
        return user_cart
    else:
        # Guest user
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
        return cart
