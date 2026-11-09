from django.db import models


class Person(models.Model):
    class Role(models.IntegerChoices):
        SUPERVISOR = 1, "supervisor"
        POSTDOC = 2, "postdoc"
        VISITING_SCHOLAR = 3, "visiting scholar"
        GRAD_STUDENT = 4, "grad student"
        RESEARCH_TECHNICIAN = 5, "research technician"
        UNDERGRAD = 6, "undergrad"

    # priority: the person's role, which also sets the order of the people page
    priority = models.PositiveIntegerField(choices=Role, null=True, blank=True)
    # personal info
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    title = models.CharField(max_length=50)
    year_start = models.PositiveIntegerField()
    year_finish = models.PositiveIntegerField(null=True, blank=True)  # Allow for ongoing members
    position_after_finish = models.CharField(max_length=50, null=True, blank=True)

    # advertisement
    personal_website = models.URLField(null=True, blank=True)
    google_scholar = models.URLField(null=True, blank=True)
    orcid = models.CharField(max_length=19, null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    pubmed = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Education(models.Model):
    person = models.ForeignKey(Person, related_name='educations', on_delete=models.CASCADE)
    degree = models.CharField(max_length=5, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    year_earned = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} {self.school} ({self.year_earned})"
