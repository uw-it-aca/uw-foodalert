from django.conf.urls import url

from . import views
from foodalert.views import *

urlpatterns = [
    url(r'^subscribed/$', SubscribedView.as_view(), name='subscribed'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^preview/$', PreView.as_view(), name='preview'),
    url(r'^$', HomeView.as_view(), name='index'),
]
