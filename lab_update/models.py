from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    posted_at = models.DateTimeField(default=timezone.now, help_text="Date and time shown under the title")
    image = models.CharField(
        max_length=200,
        help_text="File name inside static/lab_update/, e.g. lab-retreat-2026.jpg")
    body = models.TextField(blank=True, help_text="Optional caption or text shown under the picture")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_at']  # Newest post first
