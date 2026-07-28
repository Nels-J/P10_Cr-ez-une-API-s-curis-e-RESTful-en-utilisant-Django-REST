from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    birth_date = models.DateField(verbose_name=_("Date de naissance"), null=False, blank=False)

    can_be_contacted = models.BooleanField(verbose_name=_("Peut être contacté"), default=False)
    can_be_contacted_updated_at = models.DateTimeField(
            verbose_name=_("Dernière màj. du consentement de contact"), null=True, blank=True,
    )

    can_data_be_shared = models.BooleanField(verbose_name=_("Les données peuvent être partagées"), default=False)
    can_data_be_shared_updated_at = models.DateTimeField(
            verbose_name=_("Dernière màj. du consentement de partage des données"), null=True, blank=True,
    )

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
