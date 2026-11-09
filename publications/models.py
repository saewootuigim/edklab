from django.db import models


class Publication(models.Model):
    class Type(models.TextChoices):
        ARTICLE = "Article"
        REVIEW = "Review"
        PROTOCOL = "Protocol"
        PATENT = "Patent"
        DISSERTATION = "Dissertation"

    type = models.CharField(max_length=13, default="Journal", choices=Type)
    title = models.CharField(max_length=999)
    authors = models.TextField(help_text="Comma separated list of authors")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField(blank=True, null=True)
    journal = models.CharField(max_length=255)
    volume = models.PositiveIntegerField(blank=True, null=True)
    issue = models.PositiveIntegerField(blank=True, null=True)
    pages = models.CharField(max_length=50, blank=True, null=True)
    doi = models.URLField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-year', '-month']  # Newest first
