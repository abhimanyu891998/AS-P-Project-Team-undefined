from django.urls import path

from . import  views

urlpatterns = [
    path('customers', views.CustomersAllView.as_view(), name="customers"),
    path('customer_carts/<int:customer>', views.CustomerCartsView.as_view(), name="customer-carts"),
]