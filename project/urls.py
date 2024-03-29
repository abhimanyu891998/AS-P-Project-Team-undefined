"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from project import views

urlpatterns = [
    path('orders/supplies', views.ItemsAllView.as_view(), name='items'),
    path('orders/dispatch', views.DispatchAllView.as_view(), name = 'dispatchqueue'),
    path('orders/dispatch/gencsv', views.GenerateCSVAllView.as_view(), name='generatecsv'),
    path('orders/warehouse', views.WarehouseProcessingView.as_view(), name='warehouseprocessing'),
    path('orders/warehouse/genpdf', views.WarehousePDFView.as_view(), name='warehousepdf'),
    path('orders/warehouse/packingConfirmation', views.WarehousePackConfirmation.as_view(), name='packConfirmation'),
    path('orders/myorders', views.MyOrdersView.as_view(), name='myorders'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('forgot-password', views.ForgotPassword.as_view(), name='forgotPassword'),
    path('send-link', views.SendLink.as_view(), name='sendLink'),
    path('adminView', views.AdminView.as_view(), name='admin'),
    path('update-user/', views.UpdateUser.as_view(), name='updateUser'),
    path('change-password/', views.PasswordChangeView.as_view(), name='changePassword'),
    path('clinicLocation_list/', views.ChooseClinicLocationView.as_view(), name='chooseClinicLocation'),
]
