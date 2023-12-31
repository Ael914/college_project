import weasyprint
from cart.cart import Cart
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from .order_list import OrderList

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


# Create your views here.
def order_create(request: HttpRequest):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # Очистить корзину
            cart.clear()
            # Запустить асинхронное задание
            order_created.delay(order.id)
            # задать заказ в сеансе
            request.session["order_id"] = order.id
            # сохранить в список заказов
            order_list = OrderList(request)
            order_list.add(order)
            # перенаправить к платежу
            return redirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@staff_member_required
def admin_order_detail(request: HttpRequest, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request: HttpRequest, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")],
    )
    return response


def order_list(request: HttpRequest):
    orders = OrderList(request)
    return render(request, "orders/list/order_list.html", {"order_list": orders})


def order_redirect(request: HttpRequest, order_id):
    request.session["order_id"] = order_id
    return redirect(reverse("payment:process"))
