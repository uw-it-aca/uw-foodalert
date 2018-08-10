from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'base.html'
