from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMessage

import stripe
from io import BytesIO

from .models import Category, SubCategory, Product, Cart, CartItem, Order
from .forms import ShippingForm
from .utils import generate_invoice_pdf

stripe.api_key = settings.STRIPE_SECRET_KEY

def homepage(request):
    categories = Category.objects.all()
    featured_products = Product.objects.order_by('-created_at')[:8]
    return render(request, 'ecom/index.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def product_list(request, category_slug=None, subcategory_slug=None):
    products = Product.objects.all()
    category = subcategory = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)

    return render(request, 'ecom/product_list.html', {
        'products': products,
        'category': category,
        'subcategory': subcategory
    })

def cart_view(request):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, id=cart_id)
    return render(request, 'ecom/cart.html', {
        'cart': cart,
        'items': cart.items.all(),
        'total': cart.get_total()
    })

def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
            return cart
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    # Check if item already exists
    existing_item = cart.items.filter(product=product).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        item = CartItem.objects.create(product=product, quantity=1)
        cart.items.add(item)

    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id)

    if item in cart.items.all():
        cart.items.remove(item)
        item.delete()

    return redirect('cart_view')

def checkout(request):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, id=cart_id)
    form = ShippingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping = form.save(commit=False)
        order = Order.objects.create(
            cart=cart,
            customer_name=shipping.full_name,
            customer_email=shipping.email,
            shipping_address=shipping.address_line,
            payment_status='Pending'
        )
        shipping.order = order
        shipping.save()

        intent = stripe.PaymentIntent.create(
            amount=int(cart.get_total() * 100),
            currency='usd',
            metadata={'order_id': str(order.id)}
        )
        order.stripe_payment_intent_id = intent.id
        order.save(update_fields=['stripe_payment_intent_id'])

        return render(request, 'ecom/confirm_payment.html', {
            'client_secret': intent.client_secret,
            'order': order
        })

    return render(request, 'ecom/checkout.html', {
        'cart': cart,
        'form': form
    })

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')

        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = 'Paid'
            order.is_paid = True
            order.save(update_fields=['payment_status', 'is_paid'])

            pdf_bytes = generate_invoice_pdf(order)
            if pdf_bytes:
                email = EmailMessage(
                    subject='Your RayNari Order Invoice',
                    body='Thank you for your order. Please find your invoice attached.',
                    from_email='orders@raynari.com',
                    to=[order.customer_email]
                )
                email.attach(f'invoice_order_{order.id}.pdf', pdf_bytes, 'application/pdf')
                email.send()

        except Order.DoesNotExist:
            return HttpResponse(status=404)

    return HttpResponse(status=200)