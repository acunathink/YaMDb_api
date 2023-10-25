from django.urls import path

from .views import RegistrationView, TokenView


urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', RegistrationView.as_view(), name='registration'),
]