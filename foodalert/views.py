from django.shortcuts import render
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from uw_saml.utils import is_member_of_group
from django.conf import settings
from uw_saml.decorators import group_required
from django.contrib.auth.decorators import login_required
from foodalert.models import Notification, Update, Subscription
from foodalert.serializers import NotificationSerializer, UpdateSerializer,\
        SubscriptionSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


@method_decorator(login_required(), name='dispatch')
class NotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


@method_decorator(login_required(), name='dispatch')
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

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(host=self.request.user)


@method_decorator(login_required(), name='dispatch')
class UpdateDetail(generics.RetrieveAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer


@method_decorator(login_required(), name='dispatch')
class UpdateList(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer


@method_decorator(login_required(), name='dispatch')
class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


@method_decorator(login_required(), name='dispatch')
class SubscriptionList(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)


@method_decorator(login_required(), name='dispatch')
class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['signup'] = True
        context['send'] = is_member_of_group(self.request, create_group)
        context['audit'] = is_member_of_group(self.request, audit_group)
        return context


@method_decorator(group_required(create_group), name='dispatch')
class PreView(TemplateView):
    template_name = 'preview.html'


@method_decorator(group_required(create_group), name='dispatch')
class UpdateView(TemplateView):
    template_name = 'update.html'


@method_decorator(login_required(), name='dispatch')
class SignupView(TemplateView):
    template_name = 'signup.html'


@method_decorator(login_required(), name='dispatch')
class SubscribedView(TemplateView):
    template_name = 'subscribed.html'


@method_decorator(group_required(create_group), name='dispatch')
class EndedView(TemplateView):
    template_name = 'ended.html'


@method_decorator(group_required(audit_group), name='dispatch')
class AuditView(TemplateView):
    template_name = 'audit.html'
