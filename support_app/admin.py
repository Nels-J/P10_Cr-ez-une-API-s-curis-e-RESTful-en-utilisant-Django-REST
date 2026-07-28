from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from support_app.models import Contributor, Project, User

# Register your models here, making them accessible on Django admin interface.
admin.site.register(Contributor)
admin.site.register(Project)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
            (None, {"fields": ("username", "password")}),
            (
                    _("Informations personnelles"),
                    {
                            "fields": (
                                    "birth_date",
                            )
                    },
            ),
            (
                    _("Consentements"),
                    {
                            "fields": (
                                    "can_be_contacted",
                                    "can_be_contacted_updated_at",
                                    "can_data_be_shared",
                                    "can_data_be_shared_updated_at",
                            )
                    },
            ),
            (
                    _("Permissions"),
                    {
                            "fields": (
                                    "is_active",
                                    "is_staff",
                                    "is_superuser",
                                    "groups",
                                    "user_permissions",
                            )
                    },
            ),
            (
                    _("Dates importantes"),
                    {
                            "fields": (
                                    "last_login",
                                    "date_joined",
                            )
                    },
            ),
    )

    readonly_fields = (
            "can_be_contacted",
            "can_be_contacted_updated_at",
            "can_data_be_shared",
            "can_data_be_shared_updated_at",
            "last_login",
            "date_joined",
    )

    add_fieldsets = (
            (
                    None,
                    {
                            "fields": (
                                    "username",
                                    "password1",
                                    "password2",
                                    "birth_date",
                            ),
                    },
            ),
    )

    list_display = (
            "username",
            "is_staff",
            "is_superuser",
            "is_active",
    )

    list_filter = (
            "is_superuser",
            "is_staff",
            "is_active",
    )

    search_fields = (
            "username",
    )
