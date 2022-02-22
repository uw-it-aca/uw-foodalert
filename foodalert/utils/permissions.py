from django.conf import settings
from rest_framework import permissions
from rest_framework import exceptions
from uw_saml.utils import is_member_of_group
from foodalert.models import Notification, Update, Allergen,\
        Subscription

from django.core.exceptions import ImproperlyConfigured

foodalert_authz_groups = getattr(settings, 'FOODALERT_AUTHZ_GROUPS', None)
if foodalert_authz_groups is None:
    raise ImproperlyConfigured("You haven't set 'FOODALERT_AUTHZ_GROUPS'.")

create_group = foodalert_authz_groups['create']
audit_group = foodalert_authz_groups['audit']


class IsSelf(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read or
    write it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Notification):
            return obj.host == request.user
        if isinstance(obj, Subscription):
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

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class HostRead(permissions.BasePermission):
    """
    Allows users with host tag to get a resource.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) and \
            is_member_of_group(request, create_group)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class HostCreate(permissions.BasePermission):
    """
    Allows hosts to create a resource.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return is_member_of_group(request, create_group)
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
