from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from django.utils.timezone import localdate
from django.contrib import admin

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager, TreeManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, patronymic, position, salary, password):
        if not email:
            raise ValueError('Email is required!')
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name,
                          patronymic=patronymic, position=position, salary=salary)
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, patronymic, position, salary):
        user = self.create_user(email, first_name, last_name, patronymic, position, salary, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Employee(MPTTModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, db_index=True)
    last_name = models.CharField(max_length=30, db_index=True)
    patronymic = models.CharField(max_length=30, db_index=True)
    position = models.CharField(max_length=150, db_index=True)
    employment_date = models.DateField(default=localdate)
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    head = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Head'
    )
    email = models.EmailField('Email', max_length=200, unique=True)
    is_superuser = models.BooleanField('Superuser', default=False)
    is_staff = models.BooleanField('Staff', default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'patronymic', 'position', 'salary')

    @admin.display(description='Name')
    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'

    def __str__(self):
        return self.get_full_name()

    class MPTTMeta:
        order_insertion_by = ['last_name']
        parent_attr = 'head'
