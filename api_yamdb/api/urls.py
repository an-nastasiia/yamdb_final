from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    GetJWTTokenAPIView, ReviewViewSet, SignUpAPIView,
                    TitleViewSet, UsersViewSet)


API_V1 = 'v1/'

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_pathes = [
    path('auth/signup/', SignUpAPIView.as_view()),
    path('auth/token/', GetJWTTokenAPIView.as_view()),
]

urlpatterns = [
    path(API_V1, include(auth_pathes)),
    path(API_V1, include(router_v1.urls))
]
