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


# Create your models here.
def create_profile(sender, **kwargs):
    if kwargs["created"]:
        user_profile = Profile.objects.create(user=kwargs["instance"])
@receiver(post_save, sender=create_profile)
class NewUser(models.Model, AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone_number = models.CharField(max_length=12, unique=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "email", "phone_number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
class NewUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

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
    profile_pic = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Employee(models.Model, PermissionRequiredMixin, LoginRequiredMixin):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
def upload_yard_pics(instance, filename):
    return f"uploads/yard_pics/{instance.customer.user.pk}_{instance.customer.user.username}_{filename}"    

@receiver(post_save, sender=Customer.user)
class Yard(models.Model, PermissionRequiredMixin, LoginRequiredMixin):
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


class Route(models.Model, PermissionRequiredMixin, LoginRequiredMixin):
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
class Profile(models.Model, PermissionRequiredMixin, LoginRequiredMixin):
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(default="default.jpg", upload_to=upload_profile_pics)
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, primary_key=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f"Profile created for: {self.user.username} which belongs to {self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})
    