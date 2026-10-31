from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'pin_code',
            'payment_method',
            'order_notes',
        )
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address for order tracking'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flat / House No. / Street'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment, Landmark, Area (Optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-digit PIN code'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'order_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any special delivery instructions...'}),
        }

    def clean_pin_code(self):
        pin = self.cleaned_data.get('pin_code', '').strip()
        if not pin.isdigit() or len(pin) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit Indian PIN code.")
        return pin

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip().replace(' ', '').replace('-', '')
        if len(phone) < 10:
            raise forms.ValidationError("Please provide a valid 10-digit phone number.")
        return phone
