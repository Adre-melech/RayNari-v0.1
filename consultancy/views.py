from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Inquiry
from django import forms

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['full_name', 'email', 'phone', 'message']

def homepage(request):
    services = Service.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'consultancy/index.html', {
        'services': services
    })

def service_list(request):
    services = Service.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'consultancy/service_list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    form = InquiryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        inquiry = form.save(commit=False)
        inquiry.service = service
        inquiry.save()
        return render(request, 'consultancy/thank_you.html', {'service': service})

    return render(request, 'consultancy/service_detail.html', {
        'service': service,
        'form': form
    })