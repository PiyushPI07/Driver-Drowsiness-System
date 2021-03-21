from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
import datetime

class MyAccountManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, driver_name, email, password = None):
        if not email:
            raise ValueError('Users must have an mail id')
        if not driver_name:
            raise ValueError("Driver name cannot be left empty!")
        user = self.model(
            email = self.normalize_email(email),
            driver_name = driver_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, driver_name, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            driver_name = driver_name,
        )
    
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
            

class Account(AbstractBaseUser):
    dl_number = models.CharField(verbose_name="Driving License Number", max_length=16, unique=True, null=False)
    driver_name = models.CharField(verbose_name='Driver Name', max_length=50, null=False)
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    phone_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$', message="Incorrect phone number format")
    phone_number = models.CharField(verbose_name='Phone Number', validators=[phone_regex], max_length=17, blank=True)
    emergency_phn = models.CharField(verbose_name='Emergency Phone Number', validators=[phone_regex], max_length=17, blank=True)
    
    
    
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # is_recruitment_applicant = models.BooleanField(default=False)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['driver_name', ]

    def __str__(self):
        return self.email
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
