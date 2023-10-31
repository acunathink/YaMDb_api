from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    RegistrationView, ReviewsViewSet, TitlesViewSet, TokenView,
                    UsersViewSet)

v1_router = DefaultRouter()

v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('titles', TitlesViewSet)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewsViewSet
)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\w]+)/comments',
    CommentViewSet
)
urlpatterns_auth = [
    path('token/', TokenView.as_view(), name='token'),
    path('signup/', RegistrationView.as_view(), name='registration'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]
