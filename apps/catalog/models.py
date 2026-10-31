from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.name}"
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    def get_all_descendant_ids(self):
        """Recursively get IDs of this category and all its subcategories."""
        ids = [self.id]
        for child in self.children.filter(is_active=True):
            ids.extend(child.get_all_descendant_ids())
        return ids


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:brand_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original MRP for discount calculation"
    )
    stock = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            diff = self.original_price - self.price
            return int(round((diff / self.original_price) * 100))
        return 0

    @property
    def savings(self):
        if self.original_price and self.original_price > self.price:
            return self.original_price - self.price
        return Decimal('0.00')

    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / reviews.count()
            return round(avg, 1)
        return None

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Gallery image for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size = models.CharField(max_length=30, blank=True, help_text="e.g., S, M, L, XL, 32, 34, 128GB")
    color = models.CharField(max_length=30, blank=True, help_text="e.g., Black, Navy Blue, White")
    sku = models.CharField(max_length=60, unique=True, blank=True)
    stock = models.PositiveIntegerField(default=10)
    price_override = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave blank to use base product price"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['size', 'color']

    def __str__(self):
        parts = []
        if self.size:
            parts.append(f"Size: {self.size}")
        if self.color:
            parts.append(f"Color: {self.color}")
        desc = ", ".join(parts) if parts else "Default Variant"
        return f"{self.product.name} ({desc})"

    def save(self, *args, **kwargs):
        if not self.sku:
            base_sku = self.product.sku or "SKU"
            var_part = f"{self.size}-{self.color}".strip("-")
            self.sku = f"{base_sku}-{var_part}".upper().replace(" ", "")
        super().save(*args, **kwargs)

    @property
    def effective_price(self):
        if self.price_override is not None:
            return self.price_override
        return self.product.price

    @property
    def is_in_stock(self):
        return self.stock > 0


class ProductReview(models.Model):
    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Very Good'),
        (3, '3 - Good'),
        (2, '2 - Fair'),
        (1, '1 - Poor'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    headline = models.CharField(max_length=150)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.rating}★ by {self.user.username} on {self.product.name}"
