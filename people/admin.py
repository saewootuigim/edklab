from django.contrib import admin
from .models import Person, Education

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    list_display = (
        'first_name', 'middle_name', 'last_name', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'year_start', 'year_finish')
    list_filter = ('first_name', 'last_name', 'year_start', 'year_finish')

admin.site.register(Person, PersonAdmin)