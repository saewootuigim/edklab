# opportunity/views.py
from django.views.generic import TemplateView

# Create your views here.
class JobOpeningView(TemplateView):
    template_name = 'opportunity/opportunity.html'