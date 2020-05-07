from datetime import timedelta

from django.utils.translation import ugettext as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import Token
import logging

logger = logging.getLogger('app')


class RegistrationToken(Token):
    token_type = 'registration'
    lifetime = timedelta(minutes=15)


class TemporaryJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        logger.info('Validating incoming token')
        try:
            return RegistrationToken(raw_token)
        except TokenError as e:
            logger.info('Failed: {}'.format(str(e)))
            messages.append({'token_class': RegistrationToken.__name__,
                             'token_type': RegistrationToken.token_type,
                             'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })
