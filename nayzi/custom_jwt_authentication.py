from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import ugettext as _
import logging

logger = logging.getLogger('app')


class CustomerUserQueryJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        logger.info('Validating token in CustomerUserQueryJWTAuthentication')
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            logger.info('CUQW not valid with key error')
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = get_user_model().objects.select_related('provider', 'consumer').get(
                **{api_settings.USER_ID_FIELD: user_id})
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user
