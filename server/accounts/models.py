from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        COMPANY = "COMPANY", "Company"
        CREATOR = "CREATOR", "Creator"
        ADMIN = "ADMIN", "Admin"
    
    email = models.EmailField(unique=True, null=False)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_profile_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=False)

    insta_link = models.CharField(max_length=255, null=True)
    fb_link = models.CharField(max_length=255, null=True)
    yt_link = models.CharField(max_length=255, null=True)
    x_link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.company_name


class CreatorProfile(models.Model):
    class Sex(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHERS = "OTHERS", "Others"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=Sex.choices)
    platform = models.CharField(max_length=100)

    followers = models.PositiveIntegerField()
    insta_link = models.CharField(max_length=255, null=True)
    fb_link = models.CharField(max_length=255, null=True)
    yt_link = models.CharField(max_length=255, null=True)
    x_link = models.CharField(max_length=255, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}({self.user.email})"

