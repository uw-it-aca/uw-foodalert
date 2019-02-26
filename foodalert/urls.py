from django.conf.urls import url, include

from . import views
from foodalert.views import *
from uw_saml.decorators import group_required
import uw_saml

urlpatterns = [
    url(r'^saml/', include('uw_saml.urls')),
    url('notification/', NotificationList.as_view(),
        name='notificaion_list'),
    url('notification/<int:pk>/',
        NotificationDetail.as_view(), name='notification_detail'),
    url('updates$', UpdateList.as_view(), name='update_list'),
    url('update/<int:pk>/',
        UpdateDetail.as_view(), name='update_detail'),
    url('subscription/', SubscriptionList.as_view(),
        name='subscription_list'),
    url('subscription/<int:pk>/',
        SubscriptionDetail.as_view(), name='subscription_detail'),
    url(r'^.*$', HomeView.as_view(), name='index'),
]
