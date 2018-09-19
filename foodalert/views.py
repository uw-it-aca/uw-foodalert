from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from uw_saml.utils import is_member_of_group
from django.conf import settings
from uw_saml.decorators import group_required

# Create your views here.

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
subscribe_group = settings.FOODALERT_AUTHZ_GROUPS['subscribe']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


@method_decorator(group_required(create_group), name='dispatch')
class HomeView(TemplateView):
    template_name = 'form.html'


@method_decorator(group_required(create_group), name='dispatch')
class PreView(TemplateView):
    template_name = 'preview.html'


@method_decorator(group_required(create_group), name='dispatch')
class UpdateView(TemplateView):
    template_name = 'update.html'


@method_decorator(group_required(subscribe_group), name='dispatch')
class SignupView(TemplateView):
    template_name = 'signup.html'


@method_decorator(group_required(subscribe_group), name='dispatch')
class SubscribedView(TemplateView):
    template_name = 'subscribed.html'


@method_decorator(group_required(create_group), name='dispatch')
class EndedView(TemplateView):
    template_name = 'ended.html'
