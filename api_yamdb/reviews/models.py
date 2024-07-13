from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import GenreCategory
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


class Review(models.Model):
    """Модель - отзыв к произведению"""

    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
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
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
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

    def __str__(self):
        return f'{self.author} - {self.title}- {self.text[:20]}'


class Comment(models.Model):
    """Модель - комментарий к отзыву"""

    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} - {self.review}- {self.text[:20]}'
