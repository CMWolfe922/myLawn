from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models as db_models
from django.db.models import fields as db_fields
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import Address, Customer, Yard, Route, Employee
from .models import NewUser, Profile
# first thing I am doing is creating a login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
# next I am creating a form for the user to create an account
class UserForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=12)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = NewUser
        fields = ["first_name", "last_name", "username", "email", "phone_number", "password1", "password2"]
        
class UserTypeForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ["is_employee", "is_customer"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_address", "city", "state", "zip_code"]
        
        
class YardForm(forms.ModelForm):
    class Meta:
        model = Yard
        fields = ["yard_name", "yard_address", "yard_size", "yard_type", "yard_notes"]

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ["route_id", "route_name", "route_address", "route_notes"]
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["notes", "profile_pic"]
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["notes", "profile_pic"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]
        
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ["first_name", "last_name", "email", "phone_number"]
        
class AddressUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = ["street_address", "city", "state", "zip_code"]
        
    
class YardUpdateForm(forms.ModelForm):
    class Meta:
        model = Yard
        fields = ["yard_name", "yard_address", "yard_size", "yard_type", "yard_notes"]
        

class RouteUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Route
        fields = ["route_id", "route_name", "route_address", "route_notes"] 