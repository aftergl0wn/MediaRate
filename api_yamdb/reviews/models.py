from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import ReviewCommentBaseModel


User = get_user_model()


class Genres(models.Model):
    name = models.CharField('Название', max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField('Идентификатор',
                            max_length=settings.MAX_SLUG_LENGTH,
                            unique=True
                            )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField('Название', max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField('Идентификатор',
                            max_length=settings.MAX_SLUG_LENGTH,
                            unique=True
                            )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.MAX_NAME_LENGTH)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genres, through='GenreTitle',
                                   verbose_name='Жанры')
    category = models.ForeignKey(Categories, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'произведние'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genres,
                              verbose_name='Жанры',
                              on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title,
                              verbose_name='Категория',
                              on_delete=models.SET_NULL, null=True)

    class Meta:
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
