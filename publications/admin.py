from django.contrib import admin
from .models import Publication

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'journal', 'year')
    search_fields = ('title', 'authors', 'journal')
    list_filter = ('year', 'journal')
