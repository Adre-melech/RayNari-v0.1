from django.contrib import admin
from .models import Service, Inquiry

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'service', 'is_handled', 'submitted_at']
    search_fields = ['full_name', 'email', 'message']
    list_filter = ['is_handled', 'submitted_at']