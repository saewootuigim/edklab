from collections import Counter
from django.views.generic import ListView
from .models import Person

DISPLAY_NAMES = {
    1: ('Principal Investigator', 'Principal Investigators'),
    2: ('Postdoctoral Researcher', 'Postdoctoral Researchers'),
    3: ('Visiting Scholar', 'Visiting Scholars'),
    4: ('Graduate Student', 'Graduate Students'),
    5: ('Staff', 'Staff'),
    6: ('Undergraduate Student', 'Undergraduate Students'),
}

class PeopleListView(ListView):
    model = Person
    template_name = 'people/people_list.html'
    context_object_name = 'people'

    def get_queryset(self):
        current_qs = Person.objects.filter(
            year_finish__isnull=True
        ).prefetch_related('educations').order_by('priority', 'year_start', 'first_name')

        priority_counts = Counter(p.priority for p in current_qs)

        current_members = []
        seen_priorities = set()
        for person in current_qs:
            person.is_first_of_category = person.priority not in seen_priorities
            if person.is_first_of_category:
                singular, plural = DISPLAY_NAMES.get(person.priority, ('', ''))
                person.category_label = plural if priority_counts[person.priority] > 1 else singular
                seen_priorities.add(person.priority)
            current_members.append(person)

        alumni = Person.objects.filter(
            year_finish__isnull=False
        ).prefetch_related('educations').order_by('-year_finish', 'priority')

        return {
            'current_members': current_members,
            'alum': alumni,
        }