# opportunity/urls.py
from django.urls import path
from .views import JobOpeningView

urlpatterns = [
    path('', JobOpeningView.as_view(), name='opportunity'),
]