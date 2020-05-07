from rest_framework.permissions import BasePermission

from nayzi.exceptions import HttpConflictException, HttpUnauthorizedException
from django.utils.translation import ugettext as _


class DoesOwnEntity(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id


class DoesOwnTheService(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.id == obj.service_provider.user.id:
            raise HttpUnauthorizedException(_('This service does not belong to you'))
        return True


class IsConsumer(BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user.profile_type == 'CONSUMER'):
            raise HttpUnauthorizedException(_('Your account is not created as a consumer'))
        return True


class IsConsumerVerified(BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user.consumer.is_verified):
            raise HttpUnauthorizedException(_('Your consumer account is not verified yet, please contact support'))
        return True


class IsProviderVerified(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'provider'):
            return False
        if request.user.provider.status != 'confirmed':
            raise HttpConflictException(_('You activity is not yet confirmed by system, please contact support'))
        else:
            return True


class IsIPAccessAllowed(BasePermission):
    def has_permission(self, request, view):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            return True
        else:
            return HttpUnauthorizedException(_('You dont have permission'))
