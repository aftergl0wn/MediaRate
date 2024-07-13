from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.empty_value_display = 'Не задано'


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description'
    )
    search_fields = ('name',)
    list_filter = ('category', 'genre')
    list_display_links = ('name',)


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    inlines = (TitleInline,)
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'review',
        'pub_date'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inline = CommentInline
    list_display = (
        'title',
        'author',
        'pub_date'
    )
    search_fields = ('title', 'author')
    list_filter = ('title',)
