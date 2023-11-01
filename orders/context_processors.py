from django.http import HttpRequest


def have_orders(request: HttpRequest):
    orders = "orders" in request.session
    return {"have_orders": orders}
