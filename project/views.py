# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from project.models import *

# Create your views here.




class ItemsAllView(ListView):
    model = Item



class DispatchAllView(View):
    def get(self,requests, *args, **kwargs):
        orders = Order.objects.all()
        totalWeight=0
        dispatchOrderList = []
        for order in orders:
            if order.status=='QUEUED_FOR_DISPATCH':
                if totalWeight+order.total_weight<=25:
                    dispatchOrderList.append(order)
                    print("HELLO" + order.status)
                    totalWeight = totalWeight + order.total_weight
                
        


        
        context = {
			'dispatch_order_list': dispatchOrderList
		}
        return render(requests,'project/dispatch_list.html',context)
