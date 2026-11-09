from django.urls import path
from .views import LabUpdateListView

urlpatterns = [
    path('', LabUpdateListView.as_view(), name='lab_update'),
]
