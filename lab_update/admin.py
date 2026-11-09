from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'image')
    search_fields = ('title', 'body')
    list_filter = ('posted_at',)
