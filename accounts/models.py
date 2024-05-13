from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create permission mixins
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy, reverse, resolve
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class NewUserManager(BaseUserManager):
    # Define methods for creating user and superuser
    def create_user(self, email, password=None, **extra_fields):
        # Ensure email is provided
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class NewUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    longitude = models.FloatField(max_length=10 ,blank=True, null=True)
    latitude = models.FloatField(max_length=10 ,blank=True, null=True)
    
    def __str__(self):
        return f"Address belongs to: {self.user.first_name} {self.user.last_name}"
    
    def get_longitude_latitude(self):
        """Create a method that returns the longitude and latitude of the address.

        Returns:
            _type_: returns the longitude and latitude of the address.
        """
        return self.longitude, self.latitude
    
@receiver(post_save, sender=NewUser)
class Customer(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    under_contract = models.BooleanField(default=False)
    profile_pic = models.ImageField(default="images/defaults/greenish_blue_filled_person_icon.png", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Employee(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
def upload_yard_pics(instance, filename):
    return f"uploads/yard_pics/{instance.customer.user.pk}_{instance.customer.user.username}_{filename}"    

@receiver(post_save, sender=Customer.user)
class Yard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    size = models.FloatField(max_length=10)
    notes = models.TextField(blank=True, null=True)
    price = models.FloatField(max_length=10)
    discounts = models.FloatField(max_length=10, blank=True, null=True)
    image = models.ImageField(default="default.jpg", upload_to=upload_yard_pics)
    
    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}'s yard"
    
    def price_after_discount(self):
        """Create a method that calculates the price after discounts.

        Returns:
            _type_: returns the price after discounts.
        """
        base_price = self.price
        discounts = self.discounts
        if discounts > 0:
            return base_price - discounts
        elif discounts < 0.99:
            return base_price - (base_price * discounts)


def upload_job_pics(instance, filename):
    return f"uploads/job_pics/{instance.employee.user.pk}_{instance.employee.user.username}_{filename}"


class Route(models.Model):
    route_id = models.CharField(primary_key=True, max_length=5, unique=True, blank=False, null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    yards = models.ManyToManyField(Yard)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(default="default.jpg", upload_to=upload_job_pics)
    revenue = models.FloatField(max_length=10, blank=True, null=True)
    
    def add_yard_to_route(self, yard):
        """Create a method that adds a yard to the route.

        Args:
            yard (_type_): yard to be added to the route.
        """
        self.yards.add(yard)
    
    def create_revenue(self):
        """Create a method that calculates the revenue for the route.

        Returns:
            _type_: returns the revenue for the route.
        """
        revenue = 0
        for yard in self.yards:
            revenue += yard.customer.lawn.price
        return revenue
    

def upload_profile_pics(instance, filename):
    return f"uploads/profile_pics/{instance.user.pk}_{instance.user.username}_{filename}"

@receiver(post_save, sender=NewUser)
class Profile(models.Model):
    profile_type = models.CharField(choices=[("customer", "Customer"), ("employee", "Employee")], max_length=10, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(default="default.jpg", upload_to=upload_profile_pics)
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    yard = models.ForeignKey(Yard, on_delete=models.CASCADE, blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    
    
    def __str__(self):
        return f"Profile created for: {self.user.username} which belongs to {self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
