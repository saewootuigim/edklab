from django.views.generic import TemplateView


class JobOpeningView(TemplateView):
    template_name = 'opportunity/opportunity.html'
