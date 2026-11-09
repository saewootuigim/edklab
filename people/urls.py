from django.urls import path
from .views import PeopleListView

urlpatterns = [
    path('', PeopleListView.as_view(), name='people_list'),
]
