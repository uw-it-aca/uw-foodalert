from django.shortcuts import render
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView
from foodalert.models import Notification, Update
from foodalert.serializers import NotificationSerializer, UpdateSerializer
from rest_framework import generics

# Create your views here.

class NotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UpdateDetail(generics.RetrieveAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer


class UpdateList(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer


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


class EndedView(TemplateView):
    template_name = 'ended.html'
