from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import (Categories, Comment, Genre, GenreTitle, Review,
                            Title, User)

from .current_default_classes import CurrentReviewDefault, CurrentTitleDefault


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for User registration."""

    FORBIDDEN_USERNAMES = ('me',)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        """Validate that username not in list of forbiden usernames."""
        if value in self.FORBIDDEN_USERNAMES:
            raise serializers.ValidationError(f'Использовать имя {value} '
                                              'в качестве username запрещено.')
        return value


class GetJWTTokenSerializer(serializers.Serializer):
    """Serializer for creating JWT Tokens."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Validate that using correct verification_code."""
        user = get_object_or_404(User, username=data.get('username'))
        if default_token_generator.check_token(user,
                                               data.get('confirmation_code')):
            return data
        raise serializers.ValidationError('Неверный код подтверждения')


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UsersSerializerForAdmins(serializers.ModelSerializer):
    """Serializer for User model for admin use."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for model Review."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date',
        )
        validators = (
            UniqueTogetherValidator(queryset=Review.objects.all(),
                                    fields=('title', 'author')),
        )


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for model Comment."""
    review = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentReviewDefault())
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentTitleDefault())

    class Meta:
        model = Comment
        fields = (
            'id',
            'review',
            'text',
            'title',
            'author',
            'pub_date',
        )


class CategoriesSerializer(serializers.ModelSerializer):
    """Serialzer for model Categories."""

    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )


class GenresSerializer(serializers.ModelSerializer):
    """Serialzer for model Genre."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Serialazer for geting model Title."""

    category = CategoriesSerializer()
    genre = GenresSerializer(many=True,)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class TitleSerializerSave(serializers.ModelSerializer):
    """Serialazer for creating and updating model Title."""

    genre = serializers.ListField(child=serializers.SlugField())
    category = serializers.SlugField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, title):
        """Creates response using serializer TitleSerializer."""
        serializer = TitleSerializer(title)
        return serializer.data

    def create(self, validated_data):
        """Creates record in model Title."""
        genres = validated_data.pop('genre')
        category = get_object_or_404(Categories,
                                     slug=validated_data['category'])
        validated_data['category'] = category
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)

        return title

    def update(self, title, validated_data):
        """Update record in model Title."""
        genres = (validated_data.pop('genre') if 'genre'
                  in self.initial_data else [])
        category = get_object_or_404(
            Categories,
            slug=validated_data.get('category', title.category.slug))
        title.category = category
        title.name = validated_data.get('name', title.name)
        title.year = validated_data.get('year', title.year)
        title.description = validated_data.get('description',
                                               title.description)
        title.save()

        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.get_or_create(genre=current_genre, title=title)

        return title
