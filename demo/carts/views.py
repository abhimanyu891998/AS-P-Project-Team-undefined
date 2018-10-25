from django.shortcuts import render

# Create your views here.
from .models import Customer, Cart
from django.http import HttpResponse
from django.views.generic.list import ListView

class CustomersAllView(ListView):
    model = Customer


class CustomerCartsView(ListView):

    # to add the cart information for every customer
    def get_queryset(self):
        self.customer = self.kwargs['customer']
        return Cart.objects.filter(customer__pk=self.customer)

    # to add the customer data to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(pk = self.kwargs['customer'])
        return context