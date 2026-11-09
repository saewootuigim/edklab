from itertools import groupby
from operator import attrgetter

from django.views.generic import TemplateView

from .models import Person

Role = Person.Role

DISPLAY_NAMES = {
    Role.SUPERVISOR: ('Principal Investigator', 'Principal Investigators'),
    Role.POSTDOC: ('Postdoctoral Researcher', 'Postdoctoral Researchers'),
    Role.VISITING_SCHOLAR: ('Visiting Scholar', 'Visiting Scholars'),
    Role.GRAD_STUDENT: ('Graduate Student', 'Graduate Students'),
    Role.RESEARCH_TECHNICIAN: ('Research Technician', 'Research Technicians'),
    Role.UNDERGRAD: ('Undergraduate Student', 'Undergraduate Students'),
}


class PeopleListView(TemplateView):
    template_name = 'people/people_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_members = list(Person.objects.filter(
            year_finish__isnull=True
        ).prefetch_related('educations').order_by('priority', 'year_start', 'first_name'))

        # Head each role's group with its display name, plural if it has several people.
        for priority, group in groupby(current_members, key=attrgetter('priority')):
            first, *rest = group
            singular, plural = DISPLAY_NAMES.get(priority, ('', ''))
            first.is_first_of_category = True
            first.category_label = plural if rest else singular

        context['current_members'] = current_members
        # Alumni cards don't show education, so there is nothing to prefetch.
        context['alumni'] = Person.objects.filter(
            year_finish__isnull=False
        ).order_by('-year_finish', 'priority')
        return context
