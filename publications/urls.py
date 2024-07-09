from django.urls import path, re_path
from .views import PublicationListView

urlpatterns = [
    re_path(r'^(?:(?P<first_name>\w+)/(?P<last_name>\w+)/)?$', PublicationListView.as_view(), name='publication_list'),
]
