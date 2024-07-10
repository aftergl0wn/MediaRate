from django.db import models


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField(default=5)
    # rating = models.OneToOneField(RET, on_delete=models.SET_NULL,
    #                               null =True, blank=True)
    description = models.TextField()
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL, null=True)

class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Titles, on_delete=models.SET_NULL, null=True)
