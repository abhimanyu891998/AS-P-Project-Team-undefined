# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.

<<<<<<< HEAD
from project.models import Item

class ItemsAllView(ListView):
    model = Item
=======
from project.models import Item, Category

class ItemsAllView(ListView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
>>>>>>> 2aa9ae75b36a647bc4844d1f447227ad9926d601
