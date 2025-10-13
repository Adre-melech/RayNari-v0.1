from django.db import models


class RetreatHero(models.Model):
    image = models.ImageField(upload_to='retreat/hero/')
    title = models.CharField(max_length=200)
    paragraph = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RetreatAbout(models.Model):
    image = models.ImageField(upload_to='retreat/about/')
    title = models.CharField(max_length=200)
    paragraph = models.TextField()

    def __str__(self):
        return self.title

class RetreatOffer(models.Model):
    image = models.ImageField(upload_to='retreat/offers/')
    title = models.CharField(max_length=200)
    paragraph = models.TextField()

    def __str__(self):
        return self.title

class RetreatTestimonial(models.Model):
    image = models.ImageField(upload_to='retreat/testimonials/')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)  # optional for admin
    testimonial = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_user_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'User' if self.is_user_submitted else 'Admin'})"

class RetreatFAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question