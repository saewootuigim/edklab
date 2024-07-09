from django.views.generic import ListView
from django.urls import reverse
from django.shortcuts import redirect
from .models import LabMember
from datetime import date

class PeopleListView(ListView):
    model = LabMember
    template_name = 'people/people_list.html'
    context_object_name = 'people'

    def get_queryset(self):
        current_year = date.today().year
        people = {
            'current_members' : LabMember.objects.filter(year_finish__isnull=True),
            'former_members' : LabMember.objects.filter(year_finish__isnull=False),
        }
        return people