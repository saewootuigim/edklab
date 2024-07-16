from django.db import models
from django.core.validators import URLValidator

class Publication(models.Model):
    type = models.CharField(max_length=13, default="Journal",
        choices={
            "Journal":"Journal",
            "Protocol":"Protocol",
            "Patent":"Patent",
            "Dissertation":"Dissertation"})
    title = models.CharField(max_length=999)
    authors = models.TextField(help_text="Comma separated list of authors")
    year = models.PositiveIntegerField()
    journal = models.CharField(max_length=255)
    volume = models.PositiveIntegerField(blank=True, null=True)
    issue = models.PositiveIntegerField(blank=True, null=True)
    pages = models.CharField(max_length=50, blank=True, null=True)
    doi = models.URLField(validators=[URLValidator()])

    def __str__(self):
        return self.title
