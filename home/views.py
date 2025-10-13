import random
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .models import HeroSection, WhyUs, WhyUsImage, Service, ContactInfo, ContactMessage
from .forms import ContactForm
# Other Apps
from blog.models import Blog


def landing_page(request):
    hero = HeroSection.objects.first()
    why_us = WhyUs.objects.all()
    latest_image = WhyUsImage.objects.order_by('-created_at').first()
    services = Service.objects.all()
    contact = ContactInfo.objects.first()

    # ✅ Get 4 randomized recent blogs
    recent_blogs = list(Blog.objects.order_by('-created_at')[:10])  # pull top 10
    random.shuffle(recent_blogs)
    recent_blogs = recent_blogs[:4]

    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        full_message = f"[RayNariCore]\n\nFrom: {name} <{email}>\nSubject: {subject}\n\n{message}"

        # Send email
        send_mail(
            subject=f"[RayNariCore] {subject}",
            message=full_message,
            from_email=email,
            recipient_list=['query@raynari.com'],
            fail_silently=False,
        )

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully.")
        form = ContactForm()  # reset form

    return render(request, 'home/index.html', {
        'hero': hero,
        'why_us': why_us,
        'latest_image': latest_image,
        'services': services,
        'contact': contact,
        'form': form,
        'recent_blogs': recent_blogs,  # ✅ Pass to template
    })
