from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    birth_date = models.DateField(null=False, blank=False)

    can_be_contacted = models.BooleanField(default=False)
    can_be_contacted_updated_at = models.DateTimeField(null=True, blank=True)

    can_data_be_shared = models.BooleanField(default=False)
    can_data_be_shared_updated_at = models.DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ["birth_date"]

    def __str__(self) -> str:
        return self.username


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Contributor(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
