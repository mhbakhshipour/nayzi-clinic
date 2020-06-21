import jdatetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import VerificationCode, User
from authentication.tokens import RegistrationToken
from authentication.validations import is_valid_mobile, is_valid_email
from nayzi.exceptions import HttpNotFoundException, HttpForbiddenRequestException, HttpBadRequestException


def validate_mobile_number(value):
    if not is_valid_mobile(value):
        raise HttpBadRequestException(_('Invalid mobile number'))


def validate_email(value):
    if not is_valid_email(value):
        raise HttpBadRequestException(_('Invalid email'))


class SterileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=True, validators=[validate_mobile_number])
    email = serializers.EmailField(required=False)
    str_hash = serializers.CharField(required=False)
    tmp_token = serializers.CharField(read_only=True)

    def validate(self, data):
        if User.objects.filter(mobile=data['mobile'], is_staff=True):
            raise serializers.ValidationError(_('You Can Not Permission To Create User, Because You Are Staff User'))

        elif VerificationCode.objects.already_requested_verification_code(data['mobile']):
            raise serializers.ValidationError(_(
                'You already have requested a verification code. You can request vc code every {} minutes'.format(
                    settings.VERIFICATION_CODE['EXPIRATION_DURATION_MINUTES'])))

        return data

    def create(self, validated_data):

        try:
            existing_user = get_user_model().objects.get(mobile=validated_data['mobile'])
            if existing_user.verified_at is None:
                existing_user.delete()
                VerificationCode.objects.create_verification_code(validated_data['mobile'], validated_data['issued_for'], validated_data['str_hash'])
            else:
                raise IntegrityError
        except get_user_model().DoesNotExist:
            VerificationCode.objects.create_verification_code(validated_data['mobile'], validated_data['issued_for'], validated_data['str_hash'])
            pass

        user = get_user_model().objects.create(
            mobile=validated_data['mobile'],
        )
        user.save()
        user.tmp_token = RegistrationToken.for_user(user)
        return user

    class Meta:
        model = get_user_model()
        fields = ['mobile', 'first_name', 'last_name', 'email', 'national_code', 'address', 'birth_date', 'tmp_token',
                  'thumbnail', 'str_hash']


class RegistrationVerificationSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True, validators=[validate_mobile_number])
    code = serializers.CharField(required=True)

    @staticmethod
    def __validate_verification_code(code, mobile, issued_for):
        try:
            vc = VerificationCode.objects.get_if_exists(code, mobile, issued_for)
            if vc.expire_at <= timezone.now():
                raise serializers.ValidationError(_('Verification code is expired, please request a new one'))
            vc.confirm()
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError(_('Invalid verification code'))

    def validate(self, data):
        self.__validate_verification_code(data['code'], data['mobile'], 'REGISTER')
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = get_user_model().objects.get(mobile=validated_data['mobile'])
        user.verified_at = timezone.now()
        user.save()
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def to_representation(self, instance):
        return instance


class LoginInputSerializer(SterileSerializer):
    mobile = serializers.CharField(required=True)
    str_hash = serializers.CharField(required=False)
    issued_for = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            existing_user = get_user_model().objects.get(mobile=validated_data['mobile'])
            if existing_user.verified_at is None:
                raise HttpNotFoundException(_('You have not registered yet'))
            else:
                if VerificationCode.objects.already_requested_verification_code(validated_data['mobile']):
                    raise HttpForbiddenRequestException(_(
                        'You already have requested a verification code. You can request vc code every {} minutes'.format(
                            settings.VERIFICATION_CODE['EXPIRATION_DURATION_MINUTES'])))
                return VerificationCode.objects.create_verification_code(validated_data['mobile'], 'LOGIN', validated_data['str_hash'])
        except get_user_model().DoesNotExist:
            raise HttpNotFoundException(_('You have not registered yet'))


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    @staticmethod
    def validate_identifier(value):
        if is_valid_mobile(value):
            return True

        raise serializers.ValidationError(_('Invalid mobile '))

    @staticmethod
    def __validate_verification_code(code, mobile, issued_for):
        try:
            vc = VerificationCode.objects.get_if_exists(code, mobile, issued_for)
            if vc.expire_at <= timezone.now():
                VerificationCode.objects.create_verification_code(mobile, issued_for)
            vc.confirm()
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError(_('Invalid verification code'))

    def validate(self, data):
        self.__validate_verification_code(data['code'], data['mobile'], 'LOGIN')
        return data

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ForgetPasswordInputSerializer(SterileSerializer):
    mobile = serializers.CharField(required=True)
    issued_for = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return VerificationCode.objects.create_verification_code(validated_data['mobile'], 'FORGET_PASSWORD')


class ForgetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True, validators=[validate_mobile_number])
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('password', _('Password and password confirmation do not match'))
        return data

    @staticmethod
    def __validate_verification_code(code, mobile, issued_for):
        try:
            vc = VerificationCode.objects.get_if_exists(code, mobile, issued_for)
            if vc.expire_at <= timezone.now():
                raise serializers.ValidationError(_('Verification code is expired, please request a new one'))
            vc.confirm()
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError(_('Invalid verification code'))

    def update(self, instance, validated_data):
        self.__validate_verification_code(validated_data['code'], validated_data['mobile'],
                                          validated_data['issued_for'])
        user = get_user_model().objects.get(mobile=validated_data.get('mobile'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def create(self, validated_data):
        pass


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False, validators=[validate_email])

    @staticmethod
    def _transform_jalali_date_to_gregorian(jalali_date):
        return jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').togregorian().date()

    def to_internal_value(self, data):
        try:
            if 'birth_date' in data and data['birth_date'] is not None and data['birth_date'] != '':
                data['birth_date'] = self._transform_jalali_date_to_gregorian(data['birth_date'])
        except Exception:
            pass
        return super().to_internal_value(data)

    class Meta:
        model = User
        read_only_fields = ['mobile']
        fields = ('mobile', 'first_name', 'last_name', 'date_joined', 'email', 'national_code', 'address', 'birth_date',
                  'thumbnail')


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'status': 'ok', 'data': {'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}}}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data