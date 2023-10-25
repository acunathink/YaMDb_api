from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegistrationView, TokenView, UsersViewSet


v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/auth/signup/', RegistrationView.as_view(), name='registration'),

]
