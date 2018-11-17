# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import csv
from django.shortcuts import render
from django.views import View
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

from project.forms import RegistrationForm
from project.models import *
from django.conf import settings

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from datetime import datetime
from django.utils import timezone

# Create your views here.
idsForCSV = []





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
                # order.ordering_clinic = ClinicLocation.objects.get()
                # order.supplying_hospital = HospitalLocation.objects.get()
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
                temp_list.append(order)
                    
                
                
              
        
        temp_list.sort(key=lambda x: x.priority, reverse=True)
        dispatch_order_list=[]
        for order in temp_list:
            if totalWeight+order.total_weight<=23.80:
                dispatch_order_list.append(order)
                print("HELLO" + order.status)
                totalWeight = totalWeight + order.total_weight

        list_to_send=serializers.serialize('json', dispatch_order_list)
        context = {
			'dispatch_order_list': list_to_send
		}
        return render(requests,'project/dispatch_list.html',context)

 



    def post(self, request):
       


        if request.is_ajax():
            jData = json.loads(request.body)
            ids = jData["ids"]
            global idsForCSV
            idsForCSV = ids

            


            for id in ids :
                   # implement email here
                send_mail("SE", "Delivery dispatched", 'teamundefined18@gmail.com', ['manvibansal75@gmail.com'],
                fail_silently=False)
                Order.objects.filter(pk=id).update(status="DISPATCHED")
                Order.objects.filter(pk=id).update(dateDispatched=datetime.now().strftime('%Y-%m-%d %X'))

            return HttpResponse(ids)


class GenerateCSVAllView(View):

    def post(self,request):
        
        
            
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['Location Name','Latitude','Longitude','Altitude'])
        if(len(idsForCSV)>0):
            for id in idsForCSV:
                tempOrder = Order.objects.get(pk=id)
                clinicOrder = ClinicLocation.objects.get(name=tempOrder.ordering_clinic)
                clincOrderLatitude = clinicOrder.latitude
                clincOrderLongitude = clinicOrder.latitude
                clinicOrderAltitute = clinicOrder.altitude
                writer.writerow([clinicOrder.name, clincOrderLatitude, clincOrderLongitude, clinicOrderAltitute])

            hospitalDetails = HospitalLocation.objects.get(name="Queen Mary Hospital Drone Port")
            writer.writerow([hospitalDetails.name,hospitalDetails.latitude,hospitalDetails.longitude,hospitalDetails.altitude])
            

            return response
        
        else:
            return HttpResponse('')


class WarehouseProcessingView(View):

    def get(self,requests, *args, **kwargs):
        orders = Order.objects.all()

        orders_to_process= []
        for order in orders:
            if order.status=='QUEUED_FOR_PROCESSING':
                orders_to_process.append(order)


        
        processing_list=[]
        for order in orders:
            if order.status=="PROCESSING_BY_WAREHOUSE":
                processing_list.append(order)
                
              
        
        orders_to_process.sort(key=lambda x: x.priority, reverse=True)
        processing_list.sort(key=lambda x: x.priority, reverse=True)
      

        context = {
			'warehouse_order_list': serializers.serialize('json', orders_to_process),
			'processing_order_list': serializers.serialize('json', processing_list)
		}
        return render(requests,'project/warehouse_processing.html',context)


    def post(self, request):
        if request.is_ajax():
            jData = json.loads(request.body)
            id = jData["id"]
            Order.objects.filter(pk=id).update(status="PROCESSING_BY_WAREHOUSE")
            return HttpResponse()

class RegistrationView(View):
    def get(self, requests):
        form = RegistrationForm
        return render(requests, 'project/register.html', {'form': form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User()
            user.name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']

            if str(form.cleaned_data['token']).startswith('cm'):
                user.role = 1
                user.save()
                # clinicManager = ClinicManager()
                # clinicManager.user = user
                # clinic = ClinicLocation()
                # # clinicManager.clinic = clinic
                # clinicManager.save()
                return HttpResponseRedirect('/clinicLocation_list/?username=%s' % user.username)
            elif str(form.cleaned_data['token']).startswith('wp'):
                user.role = 2
                user.save()
                return HttpResponseRedirect('/login')
            elif str(form.cleaned_data['token']).startswith('di'):
                user.role = 3
                user.save()
                return HttpResponseRedirect('/login')
            elif str(form.cleaned_data['token']).startswith('ad'):
                user.role = 4
                user.save()
                return HttpResponseRedirect('/admin')
            else:
                return HttpResponseRedirect('/register')
        return HttpResponseRedirect('/register')

class ChooseClinicLocationView(View):
    def get(self, requests):
        context = {
        'locations': ClinicLocation.objects.all(),
        'username': requests.GET.get('username')
        }
        return render(requests, 'project/clinicLocation_list.html', context)
    def post(self, request):
        clinicManager = ClinicManager()
        username = request.POST.get("username")
        clinicManager.user = User.objects.get(username=username)
        clinic = request.POST.get("location")
        clinicManager.clinic = ClinicLocation.objects.get(name=clinic)
        clinicManager.save()
        return HttpResponseRedirect('/login')
