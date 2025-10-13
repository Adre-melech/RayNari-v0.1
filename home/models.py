from django.db import models

class HeroSection(models.Model):
    media = models.FileField(upload_to='hero_media/')  # image, video, gif
    title = models.CharField(max_length=200)
    paragraph = models.TextField()

    def __str__(self):
        return self.title

class WhyUs(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    paragraph = models.TextField()

    def __str__(self):
        return self.title

class WhyUsImage(models.Model):
    image = models.ImageField(upload_to='why_us/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WhyUsImage uploaded at {self.created_at}"


class Service(models.Model):
    icon = models.CharField(max_length=100)  # Bootstrap icon class or custom
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.name}"