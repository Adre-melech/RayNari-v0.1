from django import forms
from .models import RetreatTestimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = RetreatTestimonial
        fields = ['image', 'name', 'email', 'testimonial']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'testimonial': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }