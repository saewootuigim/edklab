from django.urls import path, re_path
from .views import PublicationListView

urlpatterns = [
    re_path(r'^(?:(?P<first_name>\w+)/(?P<last_name>\w+)/(?P<name_used_for_publication>.+)/)?$', PublicationListView.as_view(), name='publication_list'),
]
