from django.urls import path, include
from core.views import *
urlpatterns = [
    path("", homepage_view, name="shop_home"),
    path("shop/", shop_categories_view, name="shop"),
    path('product/<int:pk>', product_details, name="product_view"),
    path("cart/", get_shopping_cart, name="shopping_cart_view"),
    path("cart/<int:product_id>",add_to_cart, name="add_to_cart"),
    path("cart/delete/<int:product_id>", delete_from_cart, name="delete_from_cart"),
    path("contact", get_contact_page, name="contact"),
    path("checkout/", checkout_page, name="checkout"),
    path("wishlist/", wishlist_page, name="wishlist"),
    path("orders/", orders_page, name="orders"),
    path("orders/<int:pk>", single_orders_page, name="single_order"),

]
