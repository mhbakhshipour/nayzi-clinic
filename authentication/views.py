from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from authentication.serializers import *
from authentication.tokens import TemporaryJWTAuthentication
from nayzi.custom_view_mixins import ExpressiveCreateModelMixin, ExpressiveUpdateModelMixin
from nayzi.exceptions import HttpUnauthorizedException, HttpConflictException


class RegisterAPI(ExpressiveCreateModelMixin, generics.CreateAPIView):
    singular_name = 'user'
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(issued_for='REGISTER')
        except IntegrityError:
            user = get_user_model().objects.get(mobile=serializer.data['mobile'])
            if user:
                raise HttpConflictException(_('This mobile is already registered'))
            else:
                raise HttpConflictException(_(
                    'Your registration has been completed, but you have not completed your profile, please login to system to continue'))


class VerifyRegistrationAPI(ExpressiveCreateModelMixin, generics.CreateAPIView):
    serializer_class = RegistrationVerificationSerializer
    singular_name = 'tokens'

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            return super().create(request, *args, **kwargs)


class RegenerateRegisterVerificationCode(APIView):
    authentication_classes = (TemporaryJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        vc = VerificationCode.objects.requested_verification_codes(request.user.mobile, 'REGISTER')
        for v in vc:
            if v.expire_at >= timezone.now():
                raise serializers.ValidationError(_('Verification code is not expired yet!'))
        VerificationCode.objects.revoke_zombie_codes(mobile=request.user.mobile)
        VerificationCode.objects.create_verification_code(mobile=request.user.mobile, issued_for='REGISTER')
        return Response({'status': 'ok'})


class RegenerateLoginVerificationCode(APIView):
    authentication_classes = (TemporaryJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        vc = VerificationCode.objects.requested_verification_codes(request.user.mobile, 'LOGIN')
        for v in vc:
            if v.expire_at >= timezone.now():
                raise serializers.ValidationError(_('Verification code is not expired yet!'))
        VerificationCode.objects.revoke_zombie_codes(mobile=request.user.mobile)
        VerificationCode.objects.create_verification_code(mobile=request.user.mobile, issued_for='LOGIN')
        return Response({'status': 'ok'})


class LoginGenerateAPI(ExpressiveCreateModelMixin, generics.CreateAPIView):
    serializer_class = LoginInputSerializer
    singular_name = 'login'


class LoginVerifyAPI(APIView):

    def get_serializer(self):
        """ Used for swagger input inspection"""
        return LoginSerializer()

    @staticmethod
    def _authenticate(request):
        credentials = request.data
        try:
            user = get_user_model().objects.get(Q(mobile=credentials['mobile']))
        except get_user_model().DoesNotExist:
            raise HttpUnauthorizedException(_('User does not exists'))
        if user.is_superuser:
            raise HttpUnauthorizedException(_('You not permitted to login in user area'))
        if user.verified_at is None:
            raise HttpUnauthorizedException(_('Your mobile number has not been verified, please call support'))

        return user

    @staticmethod
    def _generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = self._authenticate(request)

        tokens = self._generate_tokens(user)
        return Response({'status': 'ok', 'data': {'tokens': tokens}})


class ForgetPasswordGenerateAPI(ExpressiveCreateModelMixin, generics.CreateAPIView):
    serializer_class = ForgetPasswordInputSerializer
    singular_name = 'forget_password'


class ForgetPasswordVerifyAPI(APIView):
    serializer_class = ForgetPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, instance=self.request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save(issued_for='FORGET_PASSWORD')
        return Response({'status': 'ok', 'data': None})


class UpdateProfileAPI(ExpressiveUpdateModelMixin, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    singular_name = 'profile'

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok', 'data': {self.singular_name: serializer.data}})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer
