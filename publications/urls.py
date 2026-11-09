from django.urls import re_path
from .views import PublicationListView

urlpatterns = [
    # The optional author segments (e.g. Eun/Kim/Kim E/) show the same list.
    re_path(r'^(?:(?P<first_name>\w+)/(?P<last_name>\w+)/(?P<name_used_for_publication>.+)/)?$', PublicationListView.as_view(), name='publication_list'),
]
