from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_detail, name='wishlist_detail'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move-to-cart/<int:product_id>/', views.move_to_cart, name='move_to_cart'),
]
