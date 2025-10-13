from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        unique_together = ('category', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} > {self.name}"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    product_id = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='ecom/products/')
    view_count = models.PositiveIntegerField(default=0)

    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    stock = models.PositiveIntegerField(default=0, null=True, blank=True)

    is_affiliate = models.BooleanField(default=False)
    affiliate_link = models.URLField(blank=True, null=True)

    is_engineering_partner = models.BooleanField(default=False)
    partner_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        if not self.product_id:
            prefix = slugify(self.category.name) if self.category else "product"
            self.product_id = f"{prefix}-{slugify(self.title)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return (self.product.sale_price or self.product.selling_price) * self.quantity

class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    shipping_address = models.TextField()

    payment_status = models.CharField(max_length=50, default='Pending')
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    invoice_pdf = models.FileField(upload_to='ecom/invoices/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} ({self.city})"