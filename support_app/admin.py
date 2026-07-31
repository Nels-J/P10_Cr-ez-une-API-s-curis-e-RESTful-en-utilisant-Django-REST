from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from support_app.models import Contributor, Project, User

# Register your models here, making them accessible on Django admin interface.
admin.site.register(Contributor)
admin.site.register(Project)


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
                    "can_be_contacted_updated_at",
                    "can_data_be_shared",
                    "can_data_be_shared_updated_at",
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
                    "can_be_contacted_updated_at",
                    "can_data_be_shared",
                    "can_data_be_shared_updated_at",
                )
            )
        return readonly_fields