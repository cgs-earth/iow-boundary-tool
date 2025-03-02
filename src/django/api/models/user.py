from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

from .state import State
from .utility import Utility

__all__ = ["EmailAsUsernameUserManager", "User"]


class EmailAsUsernameUserManager(BaseUserManager):
    """Manager for User objects with required role and email identifier."""

    use_in_migrations = True

    def _create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address must be provided.")
        if not role:
            raise ValueError("A role must be provided.")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, role, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, role, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, Roles.ADMINISTRATOR, password, **extra_fields)


class Roles(models.TextChoices):
    """In sync with src.app.src.constants.ROLES"""

    CONTRIBUTOR = "C"
    VALIDATOR = "V"
    ADMINISTRATOR = "A"


class User(AbstractBaseUser, PermissionsMixin):
    """Treats email as the unique identifier."""

    USERNAME_FIELD = "email"
    objects = EmailAsUsernameUserManager()

    email = models.EmailField(unique=True, validators=[EmailValidator])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    has_admin_generated_password = models.BooleanField(default=True)

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    job_title = models.CharField(max_length=127)

    role = models.CharField(
        default=Roles.CONTRIBUTOR,
        choices=Roles.choices,
        max_length=1,
    )

    utilities = models.ManyToManyField(
        Utility,
        blank=True,
        related_name="users",
    )

    states = models.ManyToManyField(
        State,
        blank=True,
        related_name="users",
    )

    def clean(self):
        if self.id and self.role == Roles.CONTRIBUTOR and not self.utilities.exists():
            raise ValidationError("Contributors must be assigned a utility.")

        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email
