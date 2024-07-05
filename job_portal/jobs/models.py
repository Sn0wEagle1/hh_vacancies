from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=1000)
    company = models.CharField(max_length=255)
    salary = models.CharField(max_length=255, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    remote = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=1000)
    company = models.CharField(max_length=255)
    salary = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    remote = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
