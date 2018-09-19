from django.conf.urls import url, include

from . import views
from foodalert.views import *
from uw_saml.decorators import group_required
import uw_saml

urlpatterns = [
    url(r'^saml/', include('uw_saml.urls')),
    url(r'^subscribed/$', SubscribedView.as_view(), name='subscribed'),
    url(r'^ended/$', EndedView.as_view(), name='ended'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^preview/$', PreView.as_view(), name='preview'),
    url(r'^$', HomeView.as_view(), name='index'),
]
