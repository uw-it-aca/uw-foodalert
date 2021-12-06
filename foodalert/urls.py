# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.conf.urls import url, include

from . import views
from foodalert.views import *
from uw_saml.decorators import group_required
import uw_saml

urlpatterns = [
    url(r'^api/v1/', include([
        url(r'^notification/$', NotificationList.as_view(),
            name='notificaion_list'),
        url(r'^notification/(?P<pk>[0-9]+)/$',
            NotificationDetail.as_view(), name='notification_detail'),
        url(r'^updates/$', UpdateList.as_view(), name='update_list'),
        url(r'^updates/(?P<pk>[0-9]+)/$',
            UpdateDetail.as_view(), name='update_detail'),
        url(r'^subscription/$', SubscriptionList.as_view(),
            name='subscription_list'),
        url(r'^subscription/(?P<pk>[0-9]+)/$',
            SubscriptionDetail.as_view(), name='subscription_detail'),
        url(r'^allergen/$', AllergensList.as_view(),
            name='allergen_list'),
        url(r'^auditlog/$', AuditList.as_view(), name='audit_log'),
        url(r'^sms/$', SmsReciver.as_view(),
            name='sms'),
    ])),
    url(r'^.*$', HomeView.as_view(), name='index'),
]
