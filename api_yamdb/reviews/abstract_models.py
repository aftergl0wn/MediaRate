from django.conf import settings
from django.db import models


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
