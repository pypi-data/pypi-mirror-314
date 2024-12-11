from model_utils.fields import MonitorField

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone

from zs_utils.json_utils import CustomJSONEncoder


__all__ = [
    "AbstractZonesmartUser",
    "CustomUserManager",
]


class CustomUserManager(BaseUserManager):
    """
    Менеджер с возможностью создать пользователя
    """

    def create_user(
        self,
        email: str,
        password: str,
        is_staff: bool = False,
        is_superuser: bool = False,
        **kwargs,
    ):
        """
        Создать пользователя
        """
        user: AbstractZonesmartUser = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **kwargs)
        user.set_password(password)
        user.save()
        return user


class AbstractZonesmartUser(AbstractBaseUser, PermissionsMixin):
    """
    Данные пользователя
    """

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = models.CharField(max_length=32, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=32, null=True, verbose_name="Фамилия")

    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")
    password_last_modified = MonitorField(monitor="password", verbose_name="Дата последнего изменения пароля")

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_superuser = models.BooleanField(default=False, verbose_name="Супер юзер")
    is_staff = models.BooleanField(default=False, verbose_name="Администратор")

    extra_data = models.JSONField(
        default=dict,
        encoder=CustomJSONEncoder,
        verbose_name="Дополнительная информация",
    )

    objects = CustomUserManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.email}"

    def set_password(self, raw_password: str, save: bool = False) -> None:
        super().set_password(raw_password=raw_password)

        self.password_last_modified = timezone.now()

        if save:
            self.save(update_fields=["password", "password_last_modified"])
