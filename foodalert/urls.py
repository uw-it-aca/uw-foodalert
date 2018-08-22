from django.conf.urls import url

from . import views
from foodalert.views import HomeView, PreView, SignupView,\
        UpdateView, EndedView

urlpatterns = [
    url(r'^ended/$', EndedView.as_view(), name='ended'),
    url(r'^update/$', UpdateView.as_view(), name='update'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^preview/$', PreView.as_view(), name='preview'),
    url(r'^$', HomeView.as_view(), name='index'),
]
