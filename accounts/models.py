from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
        Create custom user with email as username field
    '''
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ActivateAccount(models.Model):
    '''
        Activate a new account
    '''
    email = models.EmailField(_('email address'))
    token = models.CharField(max_length=30, unique=True)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.email} created at {self.create_date}'
