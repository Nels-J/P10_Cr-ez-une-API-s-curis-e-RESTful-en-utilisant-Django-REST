from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT, CASCADE
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    birth_date = models.DateField(
        verbose_name=_("Date de naissance"), null=False, blank=False
    )
    can_be_contacted = models.BooleanField(
        verbose_name=_("Peut être contacté"), default=False
    )
    can_data_be_shared = models.BooleanField(
        verbose_name=_("Les données peuvent être partagées"), default=False
    )

    REQUIRED_FIELDS = ["birth_date"]

    def __str__(self) -> str:
        return self.username


class Category(models.TextChoices):
    BACK_END = "Back-End", "Back-End"
    FRONT_END = "Front-End", "Front-End"
    IOS = "iOS", "iOS"
    ANDROID = "Android", "Android"


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=PROTECT, related_name="projects")
    created_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(
        max_length=20, choices=Category.choices, null=False, blank=False
    )


class Contributor(models.Model):
    contributor = models.ForeignKey(
        User, on_delete=PROTECT, related_name="contributions"
    )
    project = models.ForeignKey(Project, on_delete=CASCADE)
    created_time = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contributor", "project"], name="unique_project_contributor"
            )
        ]


class Tag(models.TextChoices):
    BUG = "Bug", _("Bug")
    FEATURE = "Feature", _("Feature")
    TASK = "Task", _("Task")


class Status(models.TextChoices):
    TO_DO = "To Do", _("To Do")
    IN_PROGRESS = "In Progress", _("In Progress")
    FINISHED = "Finished", _("Finished")


class Priority(models.TextChoices):
    LOW = "Low", _("Low")
    MEDIUM = "Medium", _("Medium")
    HIGH = "High", _("High")


class Issue(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=CASCADE)
    author = models.ForeignKey(User, on_delete=PROTECT, related_name="created_issues")
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )
    created_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TO_DO
    )
    priority = models.CharField(
        max_length=20, choices=Priority.choices, null=True, blank=True
    )
    tags = models.CharField(max_length=20, choices=Tag.choices, null=True, blank=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=CASCADE)
    author = models.ForeignKey(User, on_delete=PROTECT, related_name="comments")
    content = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField(default=timezone.now)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
