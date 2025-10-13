from django.contrib import admin
from .models import HeroSection, WhyUs, WhyUsImage, Service, ContactInfo, ContactMessage


admin.site.register(HeroSection)
admin.site.register(WhyUs)
admin.site.register(WhyUsImage)
admin.site.register(Service)
admin.site.register(ContactInfo)
admin.site.register(ContactMessage)
