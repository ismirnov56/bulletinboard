from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/
    Кастомная аутентификация была реализована исходя из докоментации и в соответсвии с ТЗ
"""


class BBUserManager(UserManager):

    def _create_user(self, email, phone, password, **extra_fields):
        """
            Общий метод создает и сохраняет пользователя с заданным адресом электронной почты, паролем.
        """
        email = self.normalize_email(email)
        user = BBUser(email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone=None, password=None, **extra_fields):
        """
            Вызываемый метод при создании обычного пользователя, который вызывет метод _create_user.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_stuff_user(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        assert extra_fields['is_active']
        assert extra_fields['is_staff']
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone=None, password=None, **extra_fields):
        """
            Вызываемый метод при создании суперпользователя, который вызывет метод _create_user.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        assert extra_fields['is_active']
        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, phone, password, **extra_fields)


class BBUser(AbstractUser):
    """
    Кастомная модель пользователя, установливаем поле email для аутентификации и делаем его уникальными
    Добвлен телефон, info, блокировка
    """
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    #  валидация телефона, причем допустимый номер +9(999)9999999, чтобы легче было проверять на уникальность
    phone_reg = RegexValidator(regex=r'^\+\d\(\d{3}\)\d{7}$',
                               message=_("Phone number must be entered in the format: '+9(999)9999999'"))
    phone = models.CharField(_('phone number'),
                             validators=[phone_reg],
                             max_length=14,
                             blank=False,
                             unique=True,
                             error_messages={
                                 'unique': _("A user with that phone number already exists."),
                             },
                             )
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True)
    info = models.TextField(_('text field about receiving calls'), blank=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = BBUserManager()
