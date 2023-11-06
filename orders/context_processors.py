from django.http import HttpRequest


def have_orders(request: HttpRequest):
    orders = request.session.get("orders", [])
    return {"have_orders": len(orders) > 0}
