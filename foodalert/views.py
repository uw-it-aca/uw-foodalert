from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'form.html'


class PreView(TemplateView):
    template_name = 'preview.html'


class SignupView(TemplateView):
    template_name = 'signup.html'


class UpdateView(TemplateView):
    template_name = 'update.html'


class SubscribedView(TemplateView):
    template_name = 'subscribed.html'
