from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import redirect
from .models import Person
from datetime import date

class PeopleListView(ListView):
    model = Person
    template_name = 'people/people_list.html'
    context_object_name = 'people'

    def get_queryset(self):
        # current members
        cr = Person.objects.filter(year_finish__isnull=True)
        # supervisor
        crs = cr.filter(priority=1).order_by('year_start', 'first_name')
        # postdocs
        crp = cr.filter(priority=2).order_by('year_start', 'first_name')
        # grad students
        crg = cr.filter(priority=3).order_by('year_start', 'first_name')
        # staffs
        crf = cr.filter(priority=4).order_by('year_start', 'first_name')

        # alumni
        al = Person.objects.filter(year_finish__isnull=False).order_by('-year_finish', 'priority')

        people = {
            'current' : {
                'supervisors': crs,
                'postdocs': crp,
                'gradstudents': crg,
                'staffs': crf,
            },
            'alum' : al
        }

        return people