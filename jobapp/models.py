from django.db import models

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    salary_min = models.CharField(max_length=20)
    salary_max = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.job_title
