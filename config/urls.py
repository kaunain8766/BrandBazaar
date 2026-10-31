"""
BrandBazaar URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('shop/', include('apps.catalog.urls', namespace='catalog')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('wishlist/', include('apps.wishlist.urls', namespace='wishlist')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Custom Error Handlers
handler404 = 'apps.core.views.handler404'

# Customize Django Admin branding
admin.site.site_header = "BrandBazaar Administration"
admin.site.site_title = "BrandBazaar Admin Portal"
admin.site.index_title = "Welcome to BrandBazaar Management System"
