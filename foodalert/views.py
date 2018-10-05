from django.shortcuts import render
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView
from foodalert.models import Notification, Update
from foodalert.serializers import NotificationSerializer, UpdateSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class NotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            return Response(
                data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print("failed to post")
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
