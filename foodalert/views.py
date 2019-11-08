import urllib
import logging

from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from uw_saml.decorators import group_required
from uw_saml.utils import is_member_of_group

from foodalert.models import Notification, Update, Subscription, Allergen
from foodalert.serializers import NotificationDetailSerializer, \
        UpdateDetailSerializer, UpdateListSerializer, AllergenSerializer, \
        SubscriptionDetailSerializer, SubscriptionSerializer, \
        NotificationListSerializer
from foodalert.sender import Sender
from foodalert.utils.permissions import *

# Create your views here.

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']

logger = logging.getLogger('django.request')


# Override pagination settings
class StandardPaginationResult(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'

    def get_paginated_response(self, data):
        next_pg = None
        if(self.page.has_next()):
            next_pg = self.page.next_page_number()

        previous_pg = None
        if(self.page.has_previous()):
            previous_pg = self.page.previous_page_number()

        return Response({
            'next': {
                'link': self.get_next_link(),
                'page': next_pg,
            },
            'previous': {
                'link': self.get_previous_link(),
                'page': previous_pg,
            },
            'pagesize': self.page_size,
            'count': self.page.paginator.count,
            'results': data
        })


@method_decorator(login_required(), name='dispatch')
class NotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationDetailSerializer
    permission_classes = [(IsSelf & HostRead) | AuditRead]


@method_decorator(login_required(), name='dispatch')
class NotificationList(generics.ListCreateAPIView):
    permission_classes = [((IsSelf & HostRead) | AuditRead) | HostCreate]
    filter_backends = [filters.SearchFilter]
    search_fields = ['host__username', 'event']

    def get_queryset(self):
        qs = Notification.objects.all()
        # use pagination only when 'page' query param is present
        if 'page' in self.request.query_params:
            self.pagination_class = StandardPaginationResult
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
                    if settings.FOODALERT_USE_SMS == "twilio" and\
                       sms_recipients != []:
                        Sender.send_twilio_sms(sms_recipients, message)
                    elif settings.FOODALERT_USE_SMS == "amazon":
                        Sender.send_amazon_sms(sms_recipients, message)
                    if email_recipients != []:
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
                if settings.FOODALERT_USE_SMS == "twilio" and\
                   sms_recipients != []:
                    Sender.send_twilio_sms(sms_recipients,
                                           parent.event +
                                           ' Update: ' + data['text'])
                elif settings.FOODALERT_USE_SMS == "amazon":
                    Sender.send_amazon_sms(sms_recipients,
                                           parent.event +
                                           ' Update: ' + data['text'])
                if email_recipients != []:
                    Sender.send_email(
                        parent.event + ' Update: ' + data['text'],
                        email_recipients,
                        slug
                    )
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
                "Reply YES/NO to verify/delete your number for HungryHusky"
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
                [request.data['sms_number']],
                "Reply YES/NO to verify/delete your number for HungryHusky"
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
        context['logout_url'] = settings.LOGOUT_URL
        return context


@method_decorator(login_required(), name='dispatch')
class AllergensList(generics.ListCreateAPIView):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer
    permission_classes = [HostRead | AuditRead | IsAdminUser]

    # may not need
    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)


class SmsReciver(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        url = "{}://{}{}".format(
            request.META.get(
                'HTTP_X_SCHEME',
                request.META.get('wsgi.url_scheme', '')
            ),
            request.META.get('HTTP_HOST', ''),
            request.META.get('PATH_INFO', '')
        )

        logger.info("URL: {}".format(url))
        logger.info("request.META: {}".format(request.META))
        logger.info("request.POST.dict(): {}".format(request.POST.dict()))

        request_valid = validator.validate(
            url,
            request.POST.dict(),
            request.META.get('HTTP_X_TWILIO_SIGNATURE', '')
        )

        logger.info("request_valid: {}".format(request_valid))
        if not request_valid:
            return HttpResponseForbidden()

        resp = MessagingResponse()

        try:
            sub = Subscription.objects.get(sms_number=request.data['From'])
            if not sub.number_verified:
                if request.data['Body'] == "YES":
                    resp.message(
                        'HungryHusky has verified your number.' +
                        ' Your notifications are currently paused. ' +
                        'Send RESUME to resume receiving notifications.'
                    )
                    sub.number_verified = True
                    sub.save()
                    return HttpResponse(resp)
                elif request.data['Body'] == "NO":
                    resp.message('HungryHusky has deleted your number')
                    sub.sms_number = ''
                    sub.save()
                    return HttpResponse(resp)
            if (request.data['Body'] == "RESUME" and
               sub.number_verified and not sub.send_sms):
                resp.message('HungryHusky has resumed sending you' +
                             ' more notifications. Send PAUSE to pause ' +
                             'receiving notifications.')
                sub.send_sms = True
                sub.save()
            elif (request.data['Body'] == "PAUSE" and
                  sub.number_verified and sub.send_sms):
                resp.message('HungryHusky will not send any send you any' +
                             ' more notifications. Send RESUME to resume ' +
                             'receiving notifications.')
                sub.send_sms = False
                sub.save()
            else:
                resp.message(
                    'HungryHusky did not understand that command.\n' +
                    'The available commands are:\n' +
                    (
                        (
                            "PAUSE: Pause reciving notifications."
                            if sub.send_sms else
                            "RESUME: Resume reciving notifications."
                        )
                        if sub.number_verified else
                        "YES: To verify your number."
                    )
                )
        except Subscription.DoesNotExist:
            resp.message('HungryHusky does not have this number registered.')
            return HttpResponse(resp)

        return HttpResponse(resp)
