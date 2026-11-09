from django.contrib import admin
from django.db.models import F

from .models import Education, Person


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    list_display = (
        'first_name', 'middle_name', 'last_name', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'year_start', 'year_finish')
    list_filter = ('first_name', 'last_name', 'year_start', 'year_finish')

    def get_queryset(self, request):
        # Current members (no finish year) first, then alumni by latest finish year.
        return super().get_queryset(request).order_by(F('year_finish').desc(nulls_first=True))
