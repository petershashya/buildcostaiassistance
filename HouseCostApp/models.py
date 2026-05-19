from django.db import models
from django.utils import timezone
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, user_type=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, user_type=user_type, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name=models.TextField(max_length=30,default=None)
    user_type = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group, verbose_name=_("groups"), blank=True, related_name="custom_user_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_permissions",
    )

    def __str__(self):
        return self.email


class Admin(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="admin_profile"
    )
    # Add additional fields for admin profile
class House(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    quality_of_construction = models.CharField(max_length=50)
    type_of_structure = models.CharField(max_length=50)
    construction_material = models.CharField(max_length=50)
    location_of_house = models.CharField(max_length=50)
    location_nature = models.CharField(max_length=50)
    construction_period = models.IntegerField()
    predicted_price = models.FloatField(default=0.0)
    numberfloor=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.type_of_structure} in {self.location_of_house}'
    

class HouseMap(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    map_image = models.ImageField(upload_to='house_maps/')
    result = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Map {self.id}"
    

class HouseCost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # one latest housemap only
    house_map = models.OneToOneField(
        HouseMap,
        on_delete=models.CASCADE,
        related_name='house_cost',
        null=True,
        blank=True
    )
    quality_of_construction = models.CharField(max_length=50)
    type_of_structure = models.CharField(max_length=50)
    door_material = models.CharField(max_length=50)
    window_material = models.CharField(max_length=50)
    construction_material = models.CharField(max_length=50)
    location_of_house = models.CharField(max_length=50)
    location_nature = models.CharField(max_length=50)
    construction_period = models.IntegerField()
    predicted_price = models.FloatField(default=0.0)
    numberfloor = models.IntegerField(default=1)
    ai_result = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type_of_structure} in {self.location_of_house}'
