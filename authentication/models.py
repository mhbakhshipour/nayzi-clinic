import os
import random

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.utils.translation import ugettext as _
from jalali_date import datetime2jalali

from authentication.services import send_otp
from authentication.validations import is_valid_mobile


class UserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def is_mobile(value):
        if not is_valid_mobile(value):
            raise ValueError('Invalid mobile number')

    def __create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('A mobile number should be provided')

        self.is_mobile(mobile)
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self.__create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.__create_user(mobile, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model suited for mobile number authentication"""

    mobile = models.CharField(_('mobile'), max_length=20, unique=True)
    first_name = models.CharField(_('first_name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last_name'), max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    thumbnail = models.ImageField(_('thumbnail'), upload_to=settings.UPLOAD_DIRECTORIES['user_thumbnail'], blank=True, null=True)
    email = models.CharField(_('email'), blank=True, null=True, max_length=255)
    national_code = models.CharField(_('national_code'), max_length=10, null=True, blank=True)
    address = models.TextField(_('address'), blank=True, null=True)
    birth_date = models.DateField(_('birth_date'), blank=True, null=True)
    verified_at = models.DateTimeField(_('verified_at'), blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    @staticmethod
    def get_register_status():
        return 'REGISTER'

    @staticmethod
    def get_login_status():
        return 'LOGIN'

    def jalali_created_at(self):
        return datetime2jalali(self.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

    def jalali_birth_date(self):
        if self.birth_date is not None:
            return datetime2jalali(self.birth_date).strftime('%y/%m/%d')

    def jalali_verified_at(self):
        if self.verified_at is not None:
            return datetime2jalali(self.verified_at).strftime('%y/%m/%d _ %H:%M:%S')

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class VerificationCodeManager(Manager):

    @staticmethod
    def generate_verification_code():
        """Dynamically generate a random number with dynamic length configured from settings file """
        length = settings.VERIFICATION_CODE['LENGTH']
        base = 10 ** (length - 1)
        limit = int("".join(['9' for _ in range(length)]))
        return random.randint(base, limit)

    def create_verification_code(self, mobile, issued_for, str_hash=None):
        code = self.generate_verification_code()
        if os.environ.get('KAVENEGAR_API_ACTIVE') == "1":
            send_otp(code, mobile, str_hash)
            return self.create(mobile=mobile, code=code, issued_for=issued_for)
        else:
            return self.create(mobile=mobile, code=code, issued_for=issued_for)

    def get_if_exists(self, code, mobile, issued_for):
        return self.get(code=code, mobile=mobile, confirmed_at__isnull=True, issued_for=issued_for,
                        expire_at__gt=timezone.now())

    def already_requested_verification_code(self, mobile):
        return self.filter(mobile=mobile, confirmed_at__isnull=True, expire_at__gt=timezone.now())

    def requested_verification_codes(self, mobile, issued_for):
        return self.filter(mobile=mobile, confirmed_at__isnull=True, issued_for=issued_for)

    @staticmethod
    def get_forget_password_issued_for_string():
        return 'FORGET_PASSWORD'

    @staticmethod
    def get_register_issued_for_string():
        return 'REGISTER'

    @staticmethod
    def get_login_issued_for_string():
        return 'LOGIN'

    def revoke_zombie_codes(self, mobile):
        self.filter(mobile=mobile, confirmed_at__isnull=True, revoked_at__isnull=True).update(revoked_at=timezone.now())


def calculate_expiration_date():
    return timezone.now() + timezone.timedelta(minutes=settings.VERIFICATION_CODE['EXPIRATION_DURATION_MINUTES'])


class VerificationCode(models.Model):
    issued_for_choices = (
        ('REGISTER', _('REGISTER')),
        ('LOGIN', _('LOGIN')),
        ('FORGET_PASSWORD', _('FORGET_PASSWORD'))
    )

    mobile = models.CharField(_('mobile'), max_length=255)
    code = models.CharField(_('code'), max_length=10)
    issued_for = models.CharField(_('issued_for'), max_length=20, choices=issued_for_choices)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    confirmed_at = models.DateTimeField(_('created_at'), blank=True, null=True)
    expire_at = models.DateTimeField(_('expire_at'), default=calculate_expiration_date)
    revoked_at = models.DateTimeField(_('revoked_at'), blank=True, null=True)

    objects = VerificationCodeManager()

    def confirm(self):
        self.confirmed_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'verification_codes'
        verbose_name = _('verification_code')
        verbose_name_plural = _('verification_codes')
