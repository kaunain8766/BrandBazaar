from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm, ShippingAddressForm
from .models import UserProfile
from apps.cart.utils import get_or_create_cart
from apps.wishlist.utils import get_or_create_wishlist


def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # Sync any guest cart/wishlist
            get_or_create_cart(request)
            get_or_create_wishlist(request)
            messages.success(request, f"Welcome to BrandBazaar, {user.first_name}! Your account was created successfully.")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'core:home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            guest_session_key = request.session.session_key
            user = form.get_user()
            auth_login(request, user)
            # Sync any guest cart and wishlist into user account
            get_or_create_cart(request, guest_session_key=guest_session_key)
            get_or_create_wishlist(request, guest_session_key=guest_session_key)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url if next_url else 'core:home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': request.GET.get('next', '')})


def user_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        auth_logout(request)
        messages.info(request, "You have been logged out securely.")
    return redirect('core:home')


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, instance=request.user)
        p_form = ShippingAddressForm(request.POST, instance=profile_obj)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile and shipping details have been updated.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please check the submitted information for errors.")
    else:
        u_form = UserProfileUpdateForm(instance=request.user)
        p_form = ShippingAddressForm(instance=profile_obj)

    return render(request, 'accounts/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile_obj,
    })
