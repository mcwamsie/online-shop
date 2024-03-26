import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core.Cart import Cart
from core.Recommender import get_similar_ids
from core.forms import CartAddProductForm, Billing_Form, ContactFormSubmissionsForm
from core.models import *
from online_store import settings


# Create your views here.


def homepage_view(request):
    if request.method == "GET":
        recommended = Product.objects.none()

        if request.user.is_authenticated:
            interests = Interest.objects.filter(user=request.user.id)

            print("Interests:", interests)
            ids = []
            for interest in interests:
                ids.append(interest.product_id)


            if len(ids) > 0:
                similar = get_similar_ids(ids)

                for i in similar[:16]:
                    recommended |= Product.objects.filter(id=i)

                print(recommended)

        featured = Product.objects.select_related().annotate(count=models.Count('interest')).order_by('count')[:12]
        print(featured)
        context = {
            'recommended': recommended,
            'featured': featured
        }
        return render(request, "home/home.html", context=context)


def shop_categories_view(request):
    if request.method == "GET":
        products = Product.objects.none()
        categories = Category.objects.all().order_by('name')

        for category in categories:
            category.styles = Style.objects.select_related().filter(category=category.id).annotate(
                count=models.Count('product')).order_by('name')

        brands = Brand.objects.select_related().annotate(count=models.Count('product')).order_by('name')
        # print(Brand[0].num_B)
        brand_id = request.GET.get('brand', '')
        style_id = request.GET.get('style', '')
        search = request.GET.get('search', '')
        if search != "":
            products |= Product.objects.filter(
                Q(name__contains=search) | Q(brand__name__contains=search) | Q(brand__desc__contains=search) | Q(
                    desc__contains=search) | Q(style__name__contains=search) | Q(
                    style__gender__contains=search)).order_by('-created_at')
            # products |= Product.objects.all()
        else:
            products |= Product.objects.filter(brand__name__contains=brand_id, style__name__contains=style_id).order_by(
                '-created_at')

        print(products)

        page = request.GET.get('page', 1)
        show = request.GET.get('show', 9)
        paginator = Paginator(products, show)
        try:
            pros = paginator.page(page)
        except PageNotAnInteger:
            pros = paginator.page(1)
        except EmptyPage:
            pros = paginator.page(paginator.num_pages)

        featured = Product.objects.select_related().annotate(count=models.Count('interest')).order_by('count')[:12]
        # print(featured)

        context = {
            "page_header": "category",
            "brands": brands,
            "categories": categories,
            "products": pros,
            'featured': featured
        }
        return render(request, "shop/categories.html", context=context)


def product_details(request, pk):
    if request.method == "GET":
        recommended = Product.objects.none()
        if request.user.is_authenticated:
            Interest.objects.create(user_id=request.user.id, product_id=pk)
        cart_product_form = CartAddProductForm()
        similar = get_similar_ids([pk])
        print(similar)
        for i in similar[1:7]:
            recommended |= Product.objects.filter(id=i)

        print(recommended)
        context = {
            "product": Product.objects.get(pk=pk),
            'cart_product_form': cart_product_form,
            "related": recommended
        }
        return render(request, "product/product.html", context=context)



def get_shopping_cart(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })

    return render(request, 'cart/cart.html', context={'cart': cart, 'total': cart.get_total_quantity() })


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
        messages.add_message(request, messages.SUCCESS, "Shopping Cart Updated, Successfully")
    return redirect('/store/cart/')


def delete_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('/store/cart/')


def get_contact_page(request):
    if request.method == "POST":
        form = ContactFormSubmissionsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message submitted successfully. We will get in touch")
            return redirect("contact")
    else:
        form = ContactFormSubmissionsForm()

    context = {
        'form': form,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, "contact/contact.html", context)


@login_required
def checkout_page(request):
    cart = Cart(request)
    if request.method == "POST":
        billing_form = Billing_Form(request.POST)
        if billing_form.is_valid():
            instance = billing_form.save(commit=False)
            instance.user = request.user
            instance.quantity = cart.get_total_quantity()
            instance.total_price = cart.get_total_price()
            instance.save()

            for item in cart:
                order_product = OrderProducts(
                    product=item['product'],
                    order=instance,
                    price=item['price'],
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
                order_product.save()
            messages.success(request, "Order Saved Successfully")
            cart.clear()
            return redirect("orders")
    else:
        billing_form = Billing_Form()
    return render(request, "checkout/checkout.html", context={
        'billing_form': billing_form,
        'cart': cart
    })


@login_required
def orders_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "oders/orders.html", context={
        'orders': orders
    })


@login_required
def single_orders_page(request, pk):
    order = Order.objects.none()
    products = OrderProducts.objects.none()
    try:
        order = Order.objects.get(user=request.user, id=pk)
        products = OrderProducts.objects.filter(order=order)
    except Order.DoesNotExist:
        messages.error(request, "Order Not Found")
    return render(request, "single-order.html", context={
        'order': order,
        'products': products
    })

@login_required
def wishlist_page(request):
    productId = request.GET.get('productId', None)
    if productId:
        try:
            Wishlist.objects.get(user=request.user, product_id=productId)
            messages.info(request, "Product already in wish list")
        except Wishlist.DoesNotExist:
            Wishlist.objects.create(user=request.user, product_id=productId)
            messages.success(request, "Product added to wish list")
        return redirect("wishlist")
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", context={
        'wishlist': wishlist
    })
