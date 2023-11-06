from django.conf import settings
from django.http import HttpRequest
from .models import Order


class OrderList:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        order_list = self.session.get(settings.ORDER_LIST_SESSION_ID)
        if not order_list:
            order_list = self.session[settings.ORDER_LIST_SESSION_ID] = set()
        self.order_list = order_list

    def add(self, order: Order):
        self.order_list.add(Order)
        self.save()

    def remove(self, order: Order):
        if order in self.order_list:
            self.order_list.remove(order)

    def clear(self):
        del self.session[settings.ORDER_LIST_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
