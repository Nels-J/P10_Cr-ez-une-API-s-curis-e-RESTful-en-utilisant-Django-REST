from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from support_app.models import Contributor, Project, User

# Register your models here, making them accessible on Django admin interface.
@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("project", "contributor", "created_time")
    search_fields = ("project__name", "contributor__username")
    list_filter = ("project", "contributor")


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