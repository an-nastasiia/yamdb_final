from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .abstract_models import PubDateModel
from .validators import validate_year


class Genre(models.Model):
    """Genre model."""

    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Categories(models.Model):
    """Categories model."""

    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Title model."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='category', blank=True, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(PubDateModel):
    """Review model."""

    title = models.ForeignKey(
        Title,
        verbose_name='ID произведения',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        'Текст отзыва',
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        blank=False,
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1),
        )
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                name='one_review_by_user_per_title',
                fields=('title', 'author')
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)


class Comment(PubDateModel):
    """Comment model."""

    review = models.ForeignKey(
        Review,
        verbose_name='ID отзыва',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)


class GenreTitle(models.Model):
    """many2many model for genre and title."""

    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('genre', 'title'),
            name='unique_genre_title'
        )]
        ordering = ('genre',)

    def __str__(self):
        return f'{self.title} {self.genre}'
