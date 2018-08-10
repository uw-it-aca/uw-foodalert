from django.conf.urls import url

from . import views
from foodalert.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index'),
]
