from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import VerificationCode
from authentication.tokens import RegistrationToken
from authentication.validations import is_valid_mobile, is_valid_email


def validate_mobile_number(value):
    if not is_valid_mobile(value):
        raise serializers.ValidationError(_('Invalid mobile number'))


def validate_input_password(value):
    validate_password(value)


class SterileSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(required=True, validators=[validate_mobile_number])
    email = serializers.EmailField(required=False)
    tmp_token = serializers.CharField(read_only=True)

    def validate(self, data):
        if VerificationCode.objects.already_requested_verification_code(data['mobile']):
            raise serializers.ValidationError(_(
                'You already have requested a verification code. You can request vc code every {} minutes'.format(
                    settings.VERIFICATION_CODE['EXPIRATION_DURATION_MINUTES'])))

        return data

    def create(self, validated_data):
        VerificationCode.objects.create_verification_code(validated_data['mobile'], validated_data['issued_for'])

        try:
            existing_user = get_user_model().objects.get(mobile=validated_data['mobile'])
            if existing_user.verified_at is None:
                existing_user.delete()
            else:
                raise IntegrityError
        except get_user_model().DoesNotExist:
            pass

        user = get_user_model().objects.create(
            mobile=validated_data['mobile'],
        )
        user.save()
        user.tmp_token = RegistrationToken.for_user(user)
        return user

    class Meta:
        model = get_user_model()
        fields = ['mobile', 'first_name', 'last_name', 'email', 'national_code', 'address', 'birth_date', 'tmp_token']


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
    issued_for = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return VerificationCode.objects.create_verification_code(validated_data['mobile'], 'LOGIN')


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
