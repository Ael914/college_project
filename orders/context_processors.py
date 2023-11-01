from django.http import HttpRequest


def have_orders(request: HttpRequest):
    if "orders" in request.session:
        orders = True if len(request.session["orders"]) > 0 else False
    else:
        orders = False
    return {"have_orders": orders}
