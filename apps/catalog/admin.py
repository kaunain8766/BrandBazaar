from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'alt_text', 'order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'sku', 'stock', 'price_override', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'brand',
        'price',
        'original_price',
        'stock',
        'is_active',
        'is_featured',
        'is_trending',
        'is_bestseller',
        'created_at'
    )
    list_filter = (
        'is_active',
        'is_featured',
        'is_trending',
        'is_bestseller',
        'category',
        'brand'
    )
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_active', 'is_featured', 'is_trending', 'is_bestseller')
    inlines = [ProductImageInline, ProductVariantInline]
    date_hierarchy = 'created_at'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'sku', 'stock', 'price_override', 'is_active')
    list_filter = ('is_active', 'size', 'color')
    search_fields = ('product__name', 'sku', 'size', 'color')
    list_editable = ('stock', 'price_override', 'is_active')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'headline', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('headline', 'comment', 'product__name', 'user__username')
    list_editable = ('is_approved',)
