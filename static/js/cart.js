// BrandBazaar Cart & Quantity Management

document.addEventListener('DOMContentLoaded', () => {
  // Quantity Plus / Minus controls
  const qtyWrappers = document.querySelectorAll('.quantity-control');
  qtyWrappers.forEach(wrapper => {
    const minusBtn = wrapper.querySelector('.qty-minus');
    const plusBtn = wrapper.querySelector('.qty-plus');
    const input = wrapper.querySelector('.quantity-input');

    if (minusBtn && plusBtn && input) {
      const min = parseInt(input.getAttribute('min') || '1', 10);
      const max = parseInt(input.getAttribute('max') || '99', 10);

      minusBtn.addEventListener('click', () => {
        let val = parseInt(input.value || '1', 10);
        if (val > min) {
          input.value = val - 1;
          const form = wrapper.closest('form');
          if (form && form.classList.contains('auto-submit-qty')) {
            form.submit();
          }
        }
      });

      plusBtn.addEventListener('click', () => {
        let val = parseInt(input.value || '1', 10);
        if (val < max) {
          input.value = val + 1;
          const form = wrapper.closest('form');
          if (form && form.classList.contains('auto-submit-qty')) {
            form.submit();
          }
        } else {
          alert(`Maximum available stock is ${max}.`);
        }
      });
    }
  });
});
