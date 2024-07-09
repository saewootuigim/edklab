from django.db import models

class LabMember(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    name_used_for_publication = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    year_start = models.PositiveIntegerField()
    year_finish = models.PositiveIntegerField(null=True, blank=True)  # Allow for ongoing members

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
