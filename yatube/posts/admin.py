from django.contrib import admin

from .models import Group, Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Поля, которые должны отображаться в админке
    list_display = (
        "pk",
        "text",
        "image",
        "group",
        "pub_date",
        "author",
    )
    # Интерфейс для поиска по тексту постов
    search_fields = (
        "text",
        "author",
        "group",
    )
    # Добавляем возможность редактировать группу для поста
    list_editable = ("group",)
    # Добавляем возможность фильтрации по дате
    list_filter = (
        "pub_date",
        "group",
    )
    # Это свойство сработает для всех пустых колонок
    empty_value_display = "-пусто-"


admin.site.register(Group)


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "text",
        "post",
        "created",
    )
    search_fields = (
        "text",
        "author",
        "post",
    )
    list_filter = (
        "created",
        "author",
    )
