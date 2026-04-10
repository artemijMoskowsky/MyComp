from django.urls import path, include
from .views import *

urlpatterns = [
    path("catalog/", render_catalog, name = "catalog"),
    path("product/<int:id>/", render_product, name="product"),
    path("add_to_basket/<int:id>/", add_to_basket, name="add_basket"),
    path("basket/", render_basket, name="basket"),
    path("basket/delete/<int:id>/", delete_basket, name="delete_basket"),
    path("placing_order/", render_placing_order, name="placing_order")
]