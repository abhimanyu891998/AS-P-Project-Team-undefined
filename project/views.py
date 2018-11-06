# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views import View
from django.core import serializers
from django.http import HttpResponse
from project.models import *

# Create your views here.





class ItemsAllView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'item_list': Item.objects.all(),
            'categories': Category.objects.all()
        }
        return render(request, 'project/item_list.html', context)

    def post(self, request):
        if request.is_ajax():

            jData = json.loads(request.body)
            orders = jData["obj"]
            totalWeight = jData["totalWeight"]
            priority = jData["priority"]

            order = Order()
            if totalWeight:
                order.total_weight = totalWeight
                order.priority = priority
                order.ordering_clinic = ClinicLocation.objects.get(id=1)
                order.supplying_hospital = HospitalLocation.objects.get(id=1)
                order.save()

            print(orders)
            for orderId, quant in orders.items():
                orderedItem = OrderedItem()
                orderedItem.order = Order.objects.get(id=order.id)
                orderedItem.item = Item.objects.get(id=orderId)
                orderedItem.quantity = quant
                orderedItem.save()

            return HttpResponse(orders)

# class ItemsAllView(ListView):
#     model = Item
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         return context


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

    


    def post(self, request):
        if request.is_ajax():
            jData = json.loads(request.body)
            ids = jData["ids"]   

            for id in ids :
                Order.objects.filter(pk=id).update(status="DISPATCHED")
                
            return HttpResponse(ids)



    


