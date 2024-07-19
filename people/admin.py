from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'email', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'email', 'title')
    list_filter = ('year_start', 'year_finish')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'earned_year')
    search_fields = ('school',)
    list_filter = ('degree', 'earned_year')

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('google_scholar', 'orcid', 'linkedin')
    search_fields = ('google_scholar', 'orcid', 'linkedin')

class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'middle_name', 'last_name', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'year_start', 'year_finish')
    list_filter = ('first_name', 'last_name', 'year_start', 'year_finish')

admin.site.register(Person, PersonAdmin)