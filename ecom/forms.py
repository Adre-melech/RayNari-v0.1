from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'email',
            'phone',
            'address_line',
            'city',
            'postal_code',
            'country',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Full Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            }),
            'address_line': forms.Textarea(attrs={
                'placeholder': 'Street Address',
                'class': 'form-control',
                'rows': 2
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'class': 'form-control'
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': 'Postal Code',
                'class': 'form-control'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Country',
                'class': 'form-control'
            }),
        }