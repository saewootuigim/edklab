from django.db import models
from django.core.validators import URLValidator

class Person(models.Model):
    # personal info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    title = models.CharField(max_length=50)
    year_start = models.PositiveIntegerField()
    year_finish = models.PositiveIntegerField(null=True, blank=True)  # Allow for ongoing members

    # education
    doctor_degree = models.CharField(max_length=5, null=True, blank=True)
    doctor_school = models.CharField(max_length=100, null=True, blank=True)
    doctor_earned_year = models.PositiveIntegerField(null=True, blank=True)
    master_degree = models.CharField(max_length=5, null=True, blank=True)
    master_school = models.CharField(max_length=100, null=True, blank=True)
    master_earned_year = models.PositiveIntegerField(null=True, blank=True)
    bachelor_degree = models.CharField(max_length=5, null=True, blank=True)
    bachelor_school = models.CharField(max_length=100, null=True, blank=True)
    bachelor_earned_year = models.PositiveIntegerField(null=True, blank=True)
    
    # advertisement
    google_scholar = models.URLField(validators=[URLValidator()], null=True, blank=True)
    orcid = models.CharField(max_length=19, null=True, blank=True)
    linkedin = models.URLField(validators=[URLValidator()], null=True, blank=True)
    pubmed = models.URLField(validators=[URLValidator()], null=True, blank=True)
