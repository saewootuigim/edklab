from django.views.generic import ListView
from .models import Publication
import requests
from xml.etree import ElementTree as ET

class PublicationListView(ListView):
    template_name = 'publications/publication_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        article = Publication.objects.filter(type="Article").order_by('-year','-month')
        review = Publication.objects.filter(type="Review").order_by('-year','-month')
        protocol = Publication.objects.filter(type="Protocol").order_by('-year','-month')
        patent = Publication.objects.filter(type="Patent").order_by('-year','-month')
        dissertation = Publication.objects.filter(type="Dissertation").order_by('-year','-month')
        all = Publication.objects.all().order_by('-year','-month')
        publications = {
            "article" : article,
            "review" : review,
            "protocol" : protocol,
            "patent" : patent,
            "dissertation" : dissertation,
            "all" : all
        }
        return publications

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_author'] = self.kwargs.get('name_used_for_publication', 'Miao Y')  # Pass the target author name to the context
        return context