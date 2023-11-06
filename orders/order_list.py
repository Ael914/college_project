from django.conf import settings
from django.http import HttpRequest
from .models import Order


class OrderList:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        order_list = self.session.get(settings.ORDER_LIST_SESSION_ID)
        if not order_list:
            order_list = self.session[settings.ORDER_LIST_SESSION_ID] = []
        self.order_list = order_list

    def add(self, order: Order):
        order_id = str(order.id)
        self.order_list.append(order_id)
        self.save()

    def remove(self, order: Order):
        order_id = str(order.id)
        if order_id in self.order_list:
            self.order_list.remove(order_id)
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return len(self.order_list)

    def __iter__(self):
        orders = Order.objects.filter(id__in=self.order_list)
        for order in orders:
            yield order

    def clear(self):
        del self.session[settings.ORDER_LIST_SESSION_ID]
        self.save()
