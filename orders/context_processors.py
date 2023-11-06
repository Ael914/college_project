from django.http import HttpRequest
from .order_list import OrderList


def have_orders(request: HttpRequest):
    return {"order_list": OrderList(request)}
