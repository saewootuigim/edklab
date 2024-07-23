from django.contrib import admin
from .models import Person, Education
from django.db.models import Case, When, Value, IntegerField

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = [EducationInline]
    list_display = (
        'first_name', 'middle_name', 'last_name', 'title', 'year_start', 'year_finish')
    search_fields = ('first_name', 'last_name', 'year_start', 'year_finish')
    list_filter = ('first_name', 'last_name', 'year_start', 'year_finish')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            null_year_finish=Case(
                When(year_finish__isnull=True, then=Value(0)),
                When(year_finish__isnull=False, then=Value(1)),
                output_field=IntegerField(),
            )
        ).order_by('null_year_finish', '-year_finish')

admin.site.register(Person, PersonAdmin)