# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import csv
import io
import decimal
from django.shortcuts import render, redirect
from django.views import View
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from io import BytesIO
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
from django.core.mail import EmailMessage
import hashlib
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import update_session_auth_hash



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

class AdminView(View):
    def get(self, request):
        context = {
            'users': User.objects.all().filter(changePassword=True),
        }

        if request.user.is_authenticated:
            if(self.request.user.role == 4 or self.request.user.role == 5):
                return render(request, 'project/admin_list.html', context)
        return render(request, 'project/unauthenticated.html', {})



class ForgotPassword(View):
    def post(self, request):
        jData = json.loads(request.body)
        usernameAccount = jData["username"]
        print("this is it: on forgot password view")
        print(usernameAccount)
        temp = User.objects.get(username=usernameAccount)
        temp.changePassword = True
        temp.save()
        return HttpResponse('<h1>Password change request sent!</h1>')

class PasswordChangeView(View):
    def get(self, request):
        context = {
            'form' : PasswordChangeForm(request.user)
            }
        return render(request, 'project/password_change.html', context)
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponse('<h1>Password changed!</h1>')

            # messages.success(request, 'Your password was successfully updated!')
            # return redirect('change_password')
        else:
            return HttpResponse('<h1>Password change issue!</h1>')
        
        
        

class SendLink(View):
    def post(self, request):
        jData = json.loads(request.body)
        usernameAccount = jData["username"]
        user = User.objects.get(username=usernameAccount)
        user.changePassword = False
        user.save()
        form = PasswordResetForm({'email': user.email})

        print("this is it:on send link view")
        print(usernameAccount)
        if form.is_valid():
            request = HttpRequest()
            request.META['SERVER_NAME'] = 'localhost'
            request.META['SERVER_PORT'] = '80'
            form.save(
                request= request,
                # end_mail("SE", "Delivery dispatched", 'teamundefined18@gmail.com', ['manvibansal75@gmail.com'],
                # use_https=True,
                from_email="teamundefined18@gmail.com", 
                email_template_name='registration/password_reset_email.html')
        
        
        
        return HttpResponse('<h1>Password change request sent!</h1>')


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 1 or request.user.role == 5:
                return HttpResponseRedirect('/orders/supplies')
            elif request.user.role== 2:
                return HttpResponseRedirect('/orders/warehouse')
            elif request.user.role== 3:
                return HttpResponseRedirect('/orders/dispatch')
            elif request.user.role== 4:
                return HttpResponseRedirect('/adminView')
        return HttpResponseRedirect('/login')


class UpdateUser(View):
   def get(self, request):
       user = self.request.user
       context = {
           'user': user
       }
       return render(request, 'project/update_user.html', context)

   def post(self, request):
       user = self.request.user

       user.email = request.POST.get("email")
       user.name = request.POST.get("name")
       print(request.POST.get("name"))
       user.last_name = request.POST.get("last_name")
       user.save()
       return HttpResponseRedirect('/orders/supplies')

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
            if user.role == 1 or user.role == 5:
                return HttpResponseRedirect('/orders/supplies')
            elif user.role== 2:
                return HttpResponseRedirect('/orders/warehouse')
            elif user.role== 3:
                return HttpResponseRedirect('/orders/dispatch')
            elif user.role== 4:
                return HttpResponseRedirect('/adminView')
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
        actionType = jData["actionType"]
        id = jData["id"]
        if(actionType == 'CANCEL'):
            Order.objects.filter(pk=id).delete()
        elif (actionType == 'UPDATE'):
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
        totalWeight=decimal.Decimal(0.00)
        temp_list = []
        for order in orders:
            if order.status=='QUEUED_FOR_DISPATCH':
                temp_list.append(order)





        temp_list.sort(key=lambda x: x.priority, reverse=True)
        dispatch_order_list=[]
        for order in temp_list:
            if totalWeight+ (decimal.Decimal(order.total_weight) + decimal.Decimal(1.20)) <=25.00:
                dispatch_order_list.append(order)
                totalWeight = totalWeight + decimal.Decimal(order.total_weight) + decimal.Decimal(1.20)

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
            #ids here are order ids
            for id in ids :
                order=Order.objects.get(pk=id)
                orderingClinic=order.ordering_clinic
                for clinicManager in ClinicManager.objects.all():
                    if(str(clinicManager.clinic.name) == str(orderingClinic)):
                        email=clinicManager.user.email
                        filename="details.pdf"
                        buffer = BytesIO()
                        p = canvas.Canvas("details.pdf")
                        orderItemList = OrderedItem.objects.all().filter(order=id)
                        pdfContent = 'Order ID:' + ' ' +  str(id) + ' '
                        pdfContent += 'Items: '
                        p.drawString(100,100,pdfContent)
                        ctr = 700
                        for orderedItem in orderItemList:
                            ctr = ctr - 100
                            p.drawString(100,ctr,orderedItem.item.name)
                        p.showPage()
                        p.save()

                        # Get the value of the BytesIO buffer and write it to the response.
                        pdf = buffer.getvalue()
                        buffer.close()
                        msg = EmailMessage('Order Dispatch Confirmation for Order Id '+str(id), 'Dear user,\n Your order has been dispatched.\n Please find the attached shipping label.', 'teamundefined18@gmail.com', [str(email)])
                        
                        msg.content_subtype = "html"  
                        msg.attach_file('details.pdf')
                        msg.send()


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
            orderId=order.pk
            orderItemList = OrderedItem.objects.all().filter(order=orderId)
            toSend+="<hr>"
            toSend+="<p> Order Id: "+str(order.pk)+"</p>"
            toSend+="<p>Ordering Clinic:"+ str(order.ordering_clinic) +"</p>"
            toSend+="<p> Items in Order:  </p>"
            for orderedItem in orderItemList:
                toSend+="<p> <span>"+str(orderedItem.item.name) +" </span> <span> Quantity: "+str(orderedItem.quantity) +"</p>"
            toSend+= "<td> <button id='"+str(order.pk)+"' onclick='generatePdf(this)'> Generate PDF</button> </td>"
            toSend+= "<td> <button id='"+str(order.pk)+"' onclick='sendPackingConfirmation(this)'> Pack Order</button> </td>"
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


class WarehousePackConfirmation(View):
    def post(self,request):
        if request.is_ajax():
            jData = json.loads(request.body)
            id = jData["id"]
            Order.objects.filter(pk=id).update(status="QUEUED_FOR_DISPATCH")
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
        # Order.objects.filter(pk=shippingOrderId).update(status="QUEUED_FOR_DISPATCH")
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
                    return HttpResponseRedirect('/adminView')
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
