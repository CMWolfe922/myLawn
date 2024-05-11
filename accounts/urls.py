from django.urls import include, path
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy, reverse, resolve
from .views import register, Login, profile, Logout, PasswordReset

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # existing
    path('accounts/', register, name='register'),
    path('accounts/', Login.as_view(), name='login'),
    path('accounts/', profile, name='profile'),
    path('accounts/', Logout.as_view(), name='logout'),
    path('accounts/password/', PasswordReset.as_view(), name='password_reset'),
    path('accounts/password/', PasswordReset.as_view(), name='password_reset_done'),
]