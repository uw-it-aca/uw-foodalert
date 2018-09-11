from django.conf.urls import url

from . import views
from foodalert.views import *

urlpatterns = [
    url(r'^subscribed/$', SubscribedView.as_view(), name='subscribed'),
    url(r'^ended/$', EndedView.as_view(), name='ended'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^preview/$', PreView.as_view(), name='preview'),
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^notification/$', NotificationList.as_view(), name='notificaion_list'),
    url(r'^notification/(?P<pk>[0-9]+)/$', NotificationDetail.as_view(), name='notification_detail'),
    url(r'^updates/$', UpdateList.as_view(), name='update_list'),
    url(r'^updates/(?P<pk>[0-9]+)/$', UpdateDetail.as_view(), name='update_detail'),
]
