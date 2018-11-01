# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
# Create your views here.

from project.models import Item

class ItemsAllView(ListView):
    model = Item