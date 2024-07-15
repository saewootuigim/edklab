from django.db import models
from django.core.validators import URLValidator

class Publication(models.Model):
    title = models.CharField(max_length=999)
    authors = models.TextField(help_text="Comma separated list of authors")
    journal = models.CharField(max_length=255)
    year = models.IntegerField()
    volume = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)
    pages = models.CharField(max_length=50, blank=True, null=True)
    doi = models.URLField(validators=[URLValidator()])

    def __str__(self):
        return self.title
