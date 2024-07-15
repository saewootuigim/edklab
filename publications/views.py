from django.views.generic import ListView
from .models import Publication
import requests
from xml.etree import ElementTree as ET

class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        publications = Publication.objects.all()
        return publications

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_author'] = self.kwargs.get('name_used_for_publication', 'Miao Y')  # Pass the target author name to the context
        return context