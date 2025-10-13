from django.shortcuts import render, redirect
from .models import RetreatHero, RetreatAbout, RetreatOffer, RetreatTestimonial, RetreatFAQ
from .forms import TestimonialForm
from blog.models import Blog
import random

def retreat_home(request):
    carousel_items = RetreatHero.objects.all()[:3]
    about = RetreatAbout.objects.first()
    offers = RetreatOffer.objects.all()
    faqs = RetreatFAQ.objects.all()
    testimonials = RetreatTestimonial.objects.filter(is_user_submitted=False).order_by('-submitted_at')
    user_form = TestimonialForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and user_form.is_valid():
        testimonial = user_form.save(commit=False)
        testimonial.is_user_submitted = True
        testimonial.save()
        return redirect('retreat:home')

    recent_blogs = list(Blog.objects.order_by('-created_at')[:10])
    random.shuffle(recent_blogs)
    recent_blogs = recent_blogs[:4]

    return render(request, 'retreat/index.html', {
        'carousel_items': carousel_items,
        'about': about,
        'offers': offers,
        'faqs': faqs,
        'testimonials': testimonials,
        'user_form': user_form,
        'recent_blogs': recent_blogs,
    })



# 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