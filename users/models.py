from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models

from model_utils.models import TimeStampedModel

from users.utils import user_directory_path


class UserManager(BaseUserManager):
    """Contains common Methods"""

    def create_user(self, email, password=None, **extra_fields):
        """create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that support using email instead of username"""

    email = models.EmailField(max_length=255, unique=True , db_index=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class UserFiles(TimeStampedModel):
    user = models.ForeignKey(User,related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)


    def __str__(self):
        return self.name