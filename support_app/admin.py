from django.contrib import admin

from support_app.models import Contributor, Project, User

# Register your models here to make them accessible via the Django admin interface.
admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(User)  # Assuming you have a User model in your support_app.models
