from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Categories, Genre, Review, Title
from users.models import User
from reviews.customfilters import TitleFilter
from .customviewset import CreateListDelViewCatGenSet
from .mail_templates import send_confirm_mail
from .permissions import IsAdmin, IsAdminOnly, IsAuthorOrModeratorOrAdmin
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, GetJWTTokenSerializer,
                          ReviewSerializer, SignUpSerializer, TitleSerializer,
                          TitleSerializerSave, UsersSerializer,
                          UsersSerializerForAdmins)


class SignUpAPIView(APIView):
    """View class for User registration."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = serializer.initial_data.get('username')
        if serializer.is_valid():
            user = serializer.save()
            send_confirm_mail(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            send_confirm_mail(user)
            return Response({'username': f'Пользователь {user.username} уже '
                             'существует, код подтверждения повторно '
                             'отправлен на указанную при регистрации почту'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetJWTTokenAPIView(APIView):
    """View class for User JWT Token recieve."""

    serializer_class = GetJWTTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data.get('username')
            )
            token = RefreshToken.for_user(user)
            return Response({'token': str(token.access_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(ModelViewSet):
    """View class for User model."""

    queryset = User.objects.all()
    serializer_class = UsersSerializerForAdmins
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def get_me(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UsersSerializer(request.user, data=request.data,
                                         partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    """View class for Review model."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdmin,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """View class for Comment model."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdmin,)

    def get_title(self):
        """Get tile method."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_review(self):
        """Get review method."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Get queryset method."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Create comment method."""
        review = self.get_review()
        self.get_title()
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(ModelViewSet):
    """View class for Title model."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Get serializer class method."""
        if self.action == 'create' or self.action == 'partial_update':
            return TitleSerializerSave
        return TitleSerializer


class CategoriesViewSet(CreateListDelViewCatGenSet):
    """View class for Categories model."""

    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class GenresViewSet(CreateListDelViewCatGenSet):
    """View class for Genre model."""

    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
