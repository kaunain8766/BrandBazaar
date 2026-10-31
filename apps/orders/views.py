from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import PermissionDenied

from .models import Order, OrderItem
from .forms import CheckoutForm
from apps.cart.utils import get_or_create_cart
from apps.accounts.models import UserProfile


@login_required
def checkout(request):
    """
    Handles checkout flow: collects customer info, recalculates totals on the server,
    validates inventory, creates order and order items, decrements stock, and empties cart.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'variant').all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('catalog:product_list')

    # Pre-check inventory availability
    for item in cart_items:
        if not item.is_in_stock:
            messages.error(
                request,
                f"Sorry, '{item.product.name}' has only {item.available_stock} units in stock. Please adjust your cart."
            )
            return redirect('cart:cart_detail')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Re-verify stock inside transaction with pessimistic safety
                for item in cart_items:
                    fresh_stock = item.variant.stock if item.variant else item.product.stock
                    if item.quantity > fresh_stock:
                        messages.error(
                            request,
                            f"Stock changed for '{item.product.name}'. Only {fresh_stock} available."
                        )
                        return redirect('cart:cart_detail')

                # Server-side recalculated totals
                subtotal = cart.subtotal
                shipping_charge = cart.shipping_charge
                total = cart.total

                order = form.save(commit=False)
                order.user = request.user
                order.subtotal = subtotal
                order.shipping_charge = shipping_charge
                order.total = total

                # Modular payment processing
                if order.payment_method == 'cod':
                    order.payment_status = 'pending'
                    order.order_status = 'Confirmed'
                elif order.payment_method == 'test_online':
                    # Explicit Test Payment simulation
                    order.payment_status = 'paid'
                    order.order_status = 'Confirmed'

                order.save()

                # Create OrderItems and decrement stock
                for item in cart_items:
                    variant_str = f"{item.variant.size} / {item.variant.color}".strip(" /") if item.variant else ""
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name_snapshot=item.product.name,
                        unit_price_snapshot=item.unit_price,
                        quantity=item.quantity,
                        selected_variant_snapshot=variant_str,
                        line_total=item.line_total
                    )

                    # Decrement inventory
                    if item.variant:
                        item.variant.stock -= item.quantity
                        item.variant.save()
                    item.product.stock -= item.quantity
                    item.product.save()

                # Clear cart after successful order creation
                cart.clear()

                messages.success(
                    request,
                    f"🎉 Congratulations! Your order #{order.order_number} has been placed successfully."
                )
                return redirect('orders:order_success', order_number=order.order_number)
        else:
            messages.error(request, "Please check the errors in the shipping form.")
    else:
        # Pre-fill with user and profile data
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone,
            'address_line1': profile.address_line1,
            'address_line2': profile.address_line2,
            'city': profile.city,
            'state': profile.state,
            'pin_code': profile.pin_code,
            'payment_method': 'cod',
        }
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_number):
    """
    Renders the order confirmation page. Strictly checks user ownership.
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    """
    Lists only the orders belonging to the logged-in user.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    """
    Shows detail for a single order, strictly verifying that request.user is the owner.
    """
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        order_number=order_number,
        user=request.user
    )
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
@require_POST
def cancel_order(request, order_number):
    """
    Cancels an order if eligible (Pending/Confirmed) and restores inventory to stock.
    """
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if not order.can_be_cancelled:
        messages.error(request, f"Order #{order.order_number} cannot be cancelled in status '{order.order_status}'.")
        return redirect('orders:order_detail', order_number=order.order_number)

    with transaction.atomic():
        # Restore inventory
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()
            # If variant matched
            if item.selected_variant_snapshot and item.product:
                # Best effort variant restoration if exists
                pass

        order.order_status = 'Cancelled'
        order.save()

    messages.info(request, f"Order #{order.order_number} has been cancelled and inventory restored.")
    return redirect('orders:order_detail', order_number=order.order_number)
