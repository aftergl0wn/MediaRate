from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
    genre = models.ManyToManyField(Genres, verbose_name='Жанры')
    category = models.ForeignKey(Categories, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'произведние'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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
