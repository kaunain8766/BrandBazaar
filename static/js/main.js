// BrandBazaar Main Client Utilities

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alert messages after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 5000);
  });

  // Product Gallery thumbnail switcher
  const thumbnails = document.querySelectorAll('.product-thumb-item');
  const mainImage = document.getElementById('mainProductImage');
  if (thumbnails.length && mainImage) {
    thumbnails.forEach(thumb => {
      thumb.addEventListener('click', (e) => {
        e.preventDefault();
        const targetSrc = thumb.getAttribute('data-image-url');
        if (targetSrc) {
          mainImage.src = targetSrc;
          thumbnails.forEach(t => t.classList.remove('active', 'border-primary'));
          thumb.classList.add('active', 'border-primary');
        }
      });
    });
  }

  // Wishlist AJAX toggle button helper
  const wishlistButtons = document.querySelectorAll('.wishlist-toggle-form');
  wishlistButtons.forEach(form => {
    form.addEventListener('submit', async (e) => {
      // Allow standard POST submission or AJAX if preferred
      // Normal POST fallback ensures 100% functionality even without JS
    });
  });
});
