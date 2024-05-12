from django.urls import include, path
from .views import home, set_yard_and_address, create_booking, create_review, map, secret_page

urlpatterns = [
    path("admin/", 'admin.site.urls'),
    path("", include('accounts.urls')),  # existing
    path("", include('lawn_manager.urls')),
    path('lawn_manager/', set_yard_and_address, name='update_yard_and_address'),
]