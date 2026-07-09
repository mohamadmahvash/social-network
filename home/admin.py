from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('owner', 'slug', 'created', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('created',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('owner',)


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply', 'created')
    raw_id_fields = ('user', 'post', 'reply')
