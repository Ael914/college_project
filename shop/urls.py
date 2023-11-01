from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = "shop"
urlpatterns = [
    path(_("list/"), views.order_list, name="order_list"),
    path("list/<int:order_id>", views.order_redirect, name="order_redirect"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("", views.product_list, name="product_list"),
]
