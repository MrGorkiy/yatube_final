from django.contrib import admin

from .models import Comment, Group, Post, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "image",
        "group",
        "pub_date",
        "author",
    )
    search_fields = (
        "text",
        "author",
        "group",
    )
    list_editable = ("group",)
    list_filter = (
        "pub_date",
        "group",
    )
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

@admin.register(Follow)
class FollowersAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "user",
    )
    search_fields = (
        "author",
        "user",
    )
    list_filter = (
        "author",
        "user",
    )