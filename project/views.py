# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.core import serializers

# Create your views here.



from project.models import *


class ItemsAllView(ListView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DispatchAllView(View):
    def get(self,requests, *args, **kwargs):
        orders = Order.objects.all()
        totalWeight=0
        temp_list = []
        for order in orders:
            if order.status=='QUEUED_FOR_DISPATCH':
                if totalWeight+order.total_weight<=25:
                    temp_list.append(order)
                    print("HELLO" + order.status)
                    totalWeight = totalWeight + order.total_weight
                
        

        dispatch_order_list = serializers.serialize('json', temp_list)
        context = {
			'dispatch_order_list': dispatch_order_list
		}
        return render(requests,'project/dispatch_list.html',context)

    


    def post(self,requests,*args,**kwargs):
        print (args)
        return render(request, self.template_name, {'form': form})
    


