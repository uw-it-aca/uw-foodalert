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
from foodalert.serializers import NotificationSerializer, UpdateSerializer,\
        SubscriptionSerializer, AllergenSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from foodalert.sender import Sender

# Create your views here.

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


@method_decorator(login_required(), name='dispatch')
class NotificationDetail(generics.RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def patch(self, request, pk):
        instance = self.get_object()
        serializer = NotificationSerializer(instance,
                                            data=request.data,
                                            partial=True)
        if 'ended' not in request.data or len(request.data) > 1:
            return Response({
                "Bad Request": "Patches only apply to the ended field"},
                status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required(), name='dispatch')
class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        if is_member_of_group(self.request, audit_group):
            return Notification.objects.all()
        else:
            return self.request.user.notification_set.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
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
                if sub.email != '':
                    email_recipients.append(sub.email)
                if sub.sms_number != '':
                    sms_recipients.append(str(sub.sms_number))

            message = Sender.format_message(data)

            if not settings.DEBUG:
                if settings.FOODALERT_USE_SMS == "twilio":
                    Sender.send_twilio_sms(sms_recipients, message)
                elif settings.FOODALERT_USE_SMS == "amazon":
                    Sender.send_amazon_sms(sms_recipients, message)
                Sender.send_email(message,
                                  email_recipients,
                                  slug)

            #Sender.send_email(message, email_recipients, slug)
            return Response(
                data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print("failed to post notification")
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            slug = str(data['created_time'])
            for ch in [' ', ':', '+']:
                slug = slug.replace(ch, '')

            email_recipients = []
            sms_recipients = []
            for sub in Subscription.objects.all():
                if sub.email != '':
                    email_recipients.append(sub.email)
                if sub.sms_number != '':
                    sms_recipients.append(str(sub.sms_number))

            parent = Notification.objects.get(pk=data['parent_notification'])
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
        else:
            print("failed to post update")
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        context['subscription'], created = Subscription.objects.get_or_create(
            user=self.request.user)
        context['subscription'] = context['subscription'].pk
        return context


@method_decorator(login_required(), name='dispatch')
class AllergensList(generics.ListCreateAPIView):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)
