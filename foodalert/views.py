from django.shortcuts import render
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from uw_saml.utils import is_member_of_group
from django.conf import settings
from uw_saml.decorators import group_required
from django.contrib.auth.decorators import login_required
from foodalert.models import Notification, Update, Subscription, Allergen
from foodalert.serializers import NotificationDetailSerializer, \
        UpdateDetailSerializer, UpdateListSerializer, AllergenSerializer, \
        SubscriptionDetailSerializer, SubscriptionSerializer, \
        NotificationListSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from foodalert.sender import Sender
from foodalert.utils.permissions import *

# Create your views here.

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


@method_decorator(login_required(), name='dispatch')
class NotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationDetailSerializer
    permission_classes = [(IsSelf & HostRead) | AuditRead]


@method_decorator(login_required(), name='dispatch')
class NotificationList(generics.ListCreateAPIView):
    permission_classes = [((IsSelf & HostRead) | AuditRead) | HostCreate]

    def get_queryset(self):
        qs = Notification.objects.all()
        if 'host_netid' in self.request.query_params:
            try:
                user = User.objects.get(
                    username=self.request.query_params['host_netid']
                )
                qs = qs.filter(host=user)
            except User.DoesNotExist:
                return Notification.objects.none()
        for obj in qs:
            self.check_object_permissions(self.request, obj)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NotificationListSerializer
        else:
            return NotificationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            notifs = Notification.objects.all().filter(host=self.request.user)
            if any(notif.ended for notif in notifs) or not notifs:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                data = serializer.data

                # Remove characters we can't store in db properly
                slug = str(data['time']['created'])
                for ch in [' ', ':', '+']:
                    slug = slug.replace(ch, '')

                email_recipients = []
                sms_recipients = []
                for sub in Subscription.objects.all():
                    if sub.send_email:
                        email_recipients.append(sub.email)
                    if sub.send_sms:
                        sms_recipients.append(str(sub.sms_number))

                message = Sender.format_message(data)

                if not settings.DEBUG:
                    if settings.FOODALERT_USE_SMS == "twilio":
                        Sender.send_twilio_sms(sms_recipients, message)
                    elif settings.FOODALERT_USE_SMS == "amazon":
                        Sender.send_amazon_sms(sms_recipients, message)
                    Sender.send_email(message, email_recipients, slug)

                return Response(
                    data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(
                    {"Conflict":
                        "event with this netId is already in progress"},
                    status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(host=self.request.user)


@method_decorator(login_required(), name='dispatch')
class UpdateDetail(generics.RetrieveAPIView):
    queryset = Update.objects.all()
    serializer_class = UpdateDetailSerializer
    permission_classes = [(IsSelf & HostRead) | AuditRead]


@method_decorator(login_required(), name='dispatch')
class UpdateList(generics.ListCreateAPIView):
    queryset = Update.objects.all()
    permission_classes = [((IsSelf & HostRead) | AuditRead) |
                          (IsSelf & HostCreate)]

    def get_queryset(self):
        qs = super().get_queryset()
        if 'parent_notification' in self.request.query_params:
            try:
                notif = Notification.objects.get(
                    pk=self.request.query_params['parent_notification']
                )
                qs = qs.filter(parent_notification=notif)
            except Notification.DoesNotExist:
                return Update.objects.none()
        for obj in qs:
            self.check_object_permissions(self.request, obj)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UpdateListSerializer
        else:
            return UpdateDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            parent = Notification.objects.get(
                pk=request.data['parent_notification_id']
            )
            self.check_object_permissions(self.request, parent)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            slug = str(data['created_time'])
            for ch in [' ', ':', '+']:
                slug = slug.replace(ch, '')

            email_recipients = []
            sms_recipients = []
            for sub in Subscription.objects.all():
                if sub.send_email:
                    email_recipients.append(sub.email)
                if sub.send_sms:
                    sms_recipients.append(str(sub.sms_number))

            if not settings.DEBUG:
                if settings.FOODALERT_USE_SMS == "twilio":
                    Sender.send_twilio_sms(sms_recipients,
                                           parent.event +
                                           ' Update: ' + data['text'])
                elif settings.FOODALERT_USE_SMS == "amazon":
                    Sender.send_amazon_sms(sms_recipients,
                                           parent.event +
                                           ' Update: ' + data['text'])
                Sender.send_email(parent.event + ' Update: ' + data['text'],
                                  email_recipients,
                                  slug)
            return Response(
                data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(login_required(), name='dispatch')
class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionDetailSerializer
    permission_classes = [IsSelf]

    def put(self, request, pk):
        if (not Subscription.objects.get(pk=pk).email_verified):
            if 'send_email' in request.data:
                request.data['send_email'] = False
        if (not Subscription.objects.get(pk=pk).number_verified):
            if 'send_sms' in request.data:
                request.data['send_sms'] = False
        if ('sms_number' in request.data and
                not settings.DEBUG and request.data['sms_number'] != ''):
            Sender.send_twilio_sms(
                request.data['sms_number'],
                "Test Verify"
            )
        return super().put(request, pk)

    def patch(self, request, pk):
        if (not Subscription.objects.get(pk=pk).email_verified):
            if 'send_email' in request.data:
                request.data['send_email'] = False
        if (not Subscription.objects.get(pk=pk).number_verified):
            if 'send_sms' in request.data:
                request.data['send_sms'] = False
        if ('sms_number' in request.data and
                not settings.DEBUG and request.data['sms_number'] != ''):
            Sender.send_twilio_sms(
                request.data['sms_number'],
                "Test Verify"
            )
        return super().patch(request, pk)


@method_decorator(login_required(), name='dispatch')
class SubscriptionList(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSelf]

    def get_queryset(self):
        qs = Subscription.objects.all()
        if 'netID' in self.request.query_params:
            try:
                netid = User.objects.get(
                    username=self.request.query_params['netID']
                )
                qs = qs.filter(user=netid)
            except User.DoesNotExist:
                return Subscription.objects.none()
        for obj in qs:
            self.check_object_permissions(self.request, obj)
        return qs

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            # catch invalid phone number
            try:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                data = serializer.data
                return Response(
                    data, status=status.HTTP_201_CREATED, headers=headers)
            except ValueError as error:
                return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            print("failed to post update")
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required(), name='dispatch')
class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['signup'] = True
        context['netid'] = self.request.user
        context['send'] = is_member_of_group(self.request, create_group)
        context['audit'] = is_member_of_group(self.request, audit_group)
        return context


@method_decorator(login_required(), name='dispatch')
class AllergensList(generics.ListCreateAPIView):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer
    permission_classes = [HostRead | AuditRead | IsAdminUser]

    # may not need
    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)
