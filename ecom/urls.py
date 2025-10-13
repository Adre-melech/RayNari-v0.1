from django.urls import path
from .views import (
    homepage,
    product_list,
    cart_view,
    add_to_cart,
    remove_from_cart,
    checkout,
    stripe_webhook,
)

app_name = "ecom"

urlpatterns = [
    path('', homepage, name='homepage'),
    path('products/', product_list, name='product_list'),
    path('products/<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('products/<slug:category_slug>/<slug:subcategory_slug>/', product_list, name='product_list_by_subcategory'),

    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

    path('checkout/', checkout, name='checkout'),
    path('stripe-webhook/', stripe_webhook, name='stripe_webhook'),
]