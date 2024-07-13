from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
