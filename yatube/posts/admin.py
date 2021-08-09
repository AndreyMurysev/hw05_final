from django.contrib import admin

from .models import Comment, Group, Post

VOID = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Для настройки отображения модели в интерфейсе
    админки применяют класс ModelAdmin.
    """
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text', )
    list_filter = ('pub_date', )
    empty_value_display = VOID


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title', )
    empty_value_display = VOID


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'post', 'created')
    empty_value_display = VOID
