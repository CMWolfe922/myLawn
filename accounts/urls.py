from django.urls import include, path
from .views import register

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # existing
    path('accounts/', register, name='register'),  # new
]