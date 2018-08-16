from django.conf.urls import url

from . import views
from foodalert.views import HomeView, PreView

urlpatterns = [
    url(r'^preview/$', PreView.as_view(), name='preview'),
    url(r'^$', HomeView.as_view(), name='index'),
]
