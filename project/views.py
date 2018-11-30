# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import csv
import io
from django.shortcuts import render
from django.views import View
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

from project.forms import RegistrationForm
from project.models import *
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from datetime import datetime
from django.core import signing
from .forms import LoginForm, TokenForm
from django.http import HttpResponseRedirect
import hashlib

# Create your views here.
idsForCSV = []

class TokenSendView(View):
    def get(self, request):
        form = TokenForm
        return render(request, 'project/send_token.html', {'form':form})
    def post(self, request):
        email = request.POST['email']
        role = request.POST['role']
        token = role + signing.dumps({'email':email})
        send_mail("Registration Token for ASP", token, 'teamundefined18@gmail.com', [email], fail_silently=False)

        # print(signing.loads(token[2:]))

        return HttpResponse('<h1>Token sent!</h1>')

class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, 'project/login.html', {'form':form})
    def post(self,request):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 1:
                return HttpResponseRedirect('/orders/supplies')
            elif user.role== 2:
                return HttpResponseRedirect('/orders/warehouse')
            elif user.role== 3:
                return HttpResponseRedirect('/orders/dispatch')
        return render(request, 'project/login.html', {'form':LoginForm, 'error':'Invalid username or password!'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')

class MyOrdersView(View):
    def get(self, request, *args, **kwargs):
        myorders = Order.objects.all().filter(ordering_clinic = ClinicManager.objects.get(user=self.request.user).clinic)
        context = {
            'myorders': myorders
        }
        if request.user.is_authenticated:
            if(self.request.user.role == 1 or self.request.user.role == 5):
                return render(request, 'project/my_orders.html', context)
        return render(request, 'project/unauthenticated.html', {})

    def post(self, request):
        jData = json.loads(request.body)
        action = jData["action"]
        if(action.type == 'CANCEL'):
            print "Cancel this order!"  
            print action.id
        elif (action.type == 'UPDATE'):
            id = action.id
            Order.objects.all().filter(pk=id).update(status="DELIVERED")
            Order.objects.all().filter(pk=id).update(dateDelivered=datetime.now().strftime('%Y-%m-%d %X'))
            
        
        return HttpResponse(request)

class ItemsAllView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'item_list': Item.objects.all(),
            'categories': Category.objects.all()
        }

        if request.user.is_authenticated:
            if(self.request.user.role == 1 or self.request.user.role == 5):
                return render(request, 'project/item_list.html', context)
        return render(request, 'project/unauthenticated.html', {})



    def post(self, request):
        if request.is_ajax():

            jData = json.loads(request.body)
            orders = jData["obj"]
            totalWeight = jData["totalWeight"]
            priority = jData["priority"]

            order = Order()
            if totalWeight:
                order.total_weight = totalWeight
                print(self.request.user)
                order.ordering_clinic = ClinicManager.objects.get(user=self.request.user).clinic
                order.priority = priority
                # order.ordering_clinic = ClinicLocation.objects.get()

                order.supplying_hospital = HospitalLocation.objects.get(name="Queen Mary Hospital Drone Port")
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
    def get(self,request, *args, **kwargs):
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

        if request.user.is_authenticated:
            if(self.request.user.role == 3 or self.request.user.role == 5):
                return render(request, 'project/dispatch_list.html', context)
        return render(request, 'project/unauthenticated.html', {})


    def post(self, request):
        if request.is_ajax():
            jData = json.loads(request.body)
            ids = jData["ids"]
            global idsForCSV
            idsForCSV = ids

            for id in ids :
                   # implement email here
                # send_mail("SE", "Delivery dispatched", 'teamundefined18@gmail.com', ['manvibansal75@gmail.com'],
                # fail_silently=False)
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
        # print (orders_to_process[0].ordering_clinic)
        toSend=' '
        for order in processing_list:
            toSend+="<hr>"
            toSend+="<p> Order Id: "+str(order.pk)+"</p>"
            toSend+="<p>Ordering Clinic:"+ str(order.ordering_clinic) +"</p>"
            toSend+= "<td> <button id='"+str(order.pk)+"' onclick='generatePdf(this)'> Generate PDF</button> </td>"+"<hr><br><br>";
            toSend+="<hr>"



        print (toSend)
        context = {
			'warehouse_order_list': serializers.serialize('json', orders_to_process),
			'processing_order_list': toSend,
		}

        if requests.user.is_authenticated:
            if(self.request.user.role == 2 or self.request.user.role == 5):
                return render(requests, 'project/warehouse_processing.html', context)
        return render(requests, 'project/unauthenticated.html', {})

    def post(self, request):
        if request.is_ajax():
            jData = json.loads(request.body)
            id = jData["id"]
            Order.objects.filter(pk=id).update(status="PROCESSING_BY_WAREHOUSE")
            return HttpResponse()



class WarehousePDFView(View):



    def post(self, request):
        if request.is_ajax():
            jData = json.loads(request.body)
            shippingOrderId = jData["id"]


        response = HttpResponse(content_type='text/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        shippingOrder = Order.objects.get(pk=shippingOrderId)
        OrderItemList = OrderedItem.objects.all().filter(order=shippingOrderId)
        pdfContent = 'Order ID:' + ' ' +  str(shippingOrderId) + ' '
        pdfContent = pdfContent + 'Final Destination:' + ' ' + str(shippingOrder.ordering_clinic) + ' ' +  ' ' + 'Items:'
        p.drawString(100,100,pdfContent)
        ctr = 700
        for orderedItem in OrderItemList:
            ctr = ctr - 100
            p.drawString(100,ctr,orderedItem.item.name)

        # Close the PDF object cleanly, and we're done.

        p.showPage()
        p.save()
        ctr=700
        Order.objects.filter(pk=shippingOrderId).update(status="QUEUED_FOR_DISPATCH")
        Order.objects.filter(pk=shippingOrderId).update(dateProcessed=datetime.now().strftime('%Y-%m-%d %X'))

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        return response



class RegistrationView(View):
    def get(self, requests):
        form = RegistrationForm
        return render(requests, 'project/register.html', {'form': form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = User()
                user.name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['last_name']


                token = str(form.cleaned_data['token'])
                user.email = signing.loads(token[2:])['email']

                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password'])

                if token.startswith('cm'):
                    user.role = 1
                    user.save()
                    return HttpResponseRedirect('/clinicLocation_list/?username=%s' % user.username)
                elif token.startswith('wp'):
                    user.role = 2
                    user.save()
                    return HttpResponseRedirect('/login')
                elif token.startswith('di'):
                    user.role = 3
                    user.save()
                    return HttpResponseRedirect('/login')
                elif token.startswith('ad'):
                    user.role = 4
                    user.save()
                    return HttpResponseRedirect('/admin')
                else:
                    return HttpResponseRedirect('/register')

            except IntegrityError as e:
                print (e.args)
                if "UNIQUE constraint" in e.args[0]:
                    form = RegistrationForm
                    return render(request, 'project/register.html', {'form': form, 'error':'Invalid username or token!'})


        return HttpResponseRedirect('/login')

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
