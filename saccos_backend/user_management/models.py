import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, membership_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, membership_number=membership_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_number, membership_number="0000", password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('userType', User.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(email, name, phone_number, membership_number, password, **extra_fields)

class User(AbstractUser):
    ADMIN = 1
    USER = 2
    PENDING = 3
    SACCOS_ACCOUNTANT = 4
    DIT_ACCOUNTANT = 5
    CHAIRPERSON = 6
    SECRETARY = 7

    ROLE_CHOICES = (
        (ADMIN, "System Admin"),
        (USER, "System User"),
        (PENDING, "Pending"),
        (SACCOS_ACCOUNTANT, "Saccos Accountant"),
        (DIT_ACCOUNTANT, "DIT Accountant"),
        (CHAIRPERSON, "Chairperson"),
        (SECRETARY, "Secretary")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12, unique=True)
    membership_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    profile = models.ImageField(upload_to="uploads/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    slp = models.CharField(max_length=100, null=True, blank=True)
    cheo = models.CharField(max_length=100, null=True, blank=True)
    taasisi = models.CharField(max_length=100, null=True, blank=True)
    idara = models.CharField(max_length=100, null=True, blank=True)
    check_namba = models.CharField(max_length=100, null=True, blank=True)
    tarehe_ya_kuzaliwa = models.DateField(null=True, blank=True)
    tarehe_ya_kuajiriwa = models.DateField(null=True, blank=True)
    tarehe_ya_kustaafu = models.DateField(null=True, blank=True)
    hadhi_ya_ndoa = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    mtaa = models.CharField(max_length=100, null=True, blank=True)
    kata = models.CharField(max_length=100, null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    mkoa = models.CharField(max_length=100, null=True, blank=True)
    mrithi = models.CharField(max_length=100, null=True, blank=True)
    uhusiano = models.CharField(max_length=100, null=True, blank=True)
    mawasiliano_ya_mrithi = models.CharField(max_length=12, blank=True, null=True)
    status = models.BooleanField(default=False)
    userType = models.PositiveIntegerField(choices=ROLE_CHOICES, default=PENDING)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    requested_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'