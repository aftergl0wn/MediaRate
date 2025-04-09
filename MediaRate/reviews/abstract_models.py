from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GenreCategory(models.Model):
    name = models.CharField('Название', max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField('Идентификатор',
                            max_length=settings.MAX_SLUG_LENGTH,
                            unique=True
                            )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ReviewCommentBaseModel(models.Model):

    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'
