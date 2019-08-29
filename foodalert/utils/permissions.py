from django.conf import settings
from rest_framework import permissions
from rest_framework import exceptions
from uw_saml.utils import is_member_of_group
from foodalert.models import Notification, Update, Allergen,\
        Subscription

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


class IsSelf(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read or
    write it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Notification) or isinstance(obj, Subscription):
            return obj.user == request.user
        if isinstance(obj, Update):
            return obj.parent_notification.host == request.user
        raise exceptions.ValidationError("This permission is not compatible" +
                                         "with this class.", code=500)


class AuditRead(permissions.BasePermission):
    """
    Allows users with audit tag to get a resource.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) and \
            is_member_of_group(request, audit_group)


class HostRead(permissions.BasePermission):
    """
    Allows users with host tag to get a resource.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) and \
            is_member_of_group(request, create_group)


class HostCreate(permissions.BasePermission):
    """
    Allows hosts to create a resource.
    """

    def has_permission(self, request, view):
        return (request.method == "POST") and \
            is_member_of_group(request, create_group)
