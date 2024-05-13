from django.contrib import admin
from .models import NewUser, Profile, Address, Customer, Yard, Route, Employee
# Register your models here.
admin.site.register(NewUser)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Yard)
admin.site.register(Route)
admin.site.register(Employee)

