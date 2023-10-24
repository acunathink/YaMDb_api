from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/signup/', UserRegistrationView.as_view(), name='registration'),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
