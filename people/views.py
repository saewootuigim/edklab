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
        current_year = date.today().year
        people = {
            'members' : [
                Person.objects.filter(year_finish__isnull=True).order_by('priority','year_start','first_name'), # current members
                Person.objects.filter(year_finish__isnull=False).order_by('year_finish','first_name') # previous members
            ]
        }

        return people