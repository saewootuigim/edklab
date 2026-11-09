from django.views.generic import ListView
from .models import Publication


class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    context_object_name = 'publications'
    queryset = Publication.objects.exclude(type=Publication.Type.DISSERTATION)
