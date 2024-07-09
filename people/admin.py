from django.contrib import admin
from .models import LabMember

@admin.register(LabMember)
class LabMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'title', 'email')
    list_filter = ('title', 'year_start', 'year_finish')
