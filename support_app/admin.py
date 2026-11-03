from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from support_app.models import Comment, Contributor, Issue, Project, User


# Register your models here, making them accessible on Django admin interface.
@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "created_time")
    search_fields = ("project__name", "user__username")
    list_filter = ("user",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "category", "author")
    search_fields = ("name", "description", "category", "author__username")
    list_filter = ("category", "author")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "is_active", "is_staff", "is_superuser")
    search_fields = ("username",)

    fieldsets = list(UserAdmin.fieldsets)
    personal_info_title, personal_info_options = fieldsets[1]
    personal_info_fields = list(personal_info_options["fields"])
    if "birth_date" not in personal_info_fields:
        personal_info_fields.append("birth_date")
    fieldsets[1] = (
        personal_info_title,
        {"fields": tuple(personal_info_fields)},
    )

    fieldsets.append(
        (
            _("Consentements"),
            {
                "fields": (
                    "can_be_contacted",
                    "can_data_be_shared",
                ),
            },
        )
    )

    fieldsets = tuple(fieldsets)

    readonly_fields = ("last_login", "date_joined")

    add_fieldsets = (
        (
            _("Informations personnelles"),
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "birth_date",
                ),
            },
        ),
        (
            _("Consentements"),
            {
                "fields": (
                    "can_be_contacted",
                    "can_data_be_shared",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.extend(
                (
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            )
        return readonly_fields


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "author",
        "status",
        "tags",
        "priority",
        "created_time",
    )
    search_fields = ("title", "description", "project__name", "author__username")
    list_filter = ("priority", "status", "tags", "assignee", "project", "author")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Customize the queryset for the assignee field based on the project context.
        if db_field.name == "assignee":
            project_id = request.GET.get("project")

            # If project_id is not found in the GET parameters,
            # try to extract it from the URL resolver kwargs.
            resolver_kwargs = getattr(
                getattr(request, "resolver_match", None), "kwargs", {}
            )
            object_id = resolver_kwargs.get("object_id")
            if object_id:
                project_id = (
                    Issue.objects.filter(pk=object_id)
                    .values_list("project_id", flat=True)
                    .first()
                )

            # If project_id is not None, filter the queryset for assignee field to
            # only include users who are contributors to the project.
            if project_id:
                kwargs["queryset"] = User.objects.filter(
                    contributions__project_id=project_id
                ).distinct()
            else:
                kwargs["queryset"] = User.objects.none()

        # If the db_field is not "assignee", or if project_id is None,
        # fall back to the default behavior.
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "content",
        "author",
        "uuid",
        "created_time",
        "issue__id",
        "issue",
    )
    search_fields = ("content", "issue__title", "author__username", "issue__id")
    list_filter = (("issue", RelatedOnlyFieldListFilter),)
