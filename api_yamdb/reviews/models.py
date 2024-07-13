from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import GenreCategory, ReviewCommentBaseModel
from .validators import year_validator

User = get_user_model()


class Genre(GenreCategory):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(GenreCategory):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.MAX_NAME_LENGTH)
    year = models.IntegerField(validators=[year_validator],
                               verbose_name='Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitle',
                                   verbose_name='Жанры')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'произведние'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              verbose_name='Жанры',
                              on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title,
                              verbose_name='Категория',
                              on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            )
        ]
        verbose_name = 'произведние-категория'
        verbose_name_plural = 'Произведения-категории'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(ReviewCommentBaseModel):
    """Модель - отзыв к произведению"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(
                1, message='Ожидается оценка от 1 до 10'),
            MaxValueValidator(
                10, message='Ожидается оценка от 1 до 10')
        ]
    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author',
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewCommentBaseModel):
    """Модель - комментарий к отзыву"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
