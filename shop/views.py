from cart.forms import CartAddProductForm
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

from .models import Category, Product
from .recommender import Recommender


# Create your views here.
def product_list(request: HttpRequest, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
        )
        products = products.filter(category=category)
    return render(
        request,
        "shop/product/list.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
        },
    )


def product_detail(request: HttpRequest, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )


def order_list(request: HttpRequest):
    orders = []
    for id in request.session["orders"][::-1]:
        order = get_object_or_404(Order, id=id)
        if not order.paid:
            orders += [
                order,
            ]
    return render(request, "shop/list/order_list.html", {"orders": orders})


def order_redirect(request: HttpRequest, order_id):
    request.session["order_id"] = order_id
    return redirect(reverse("payment:process"))
