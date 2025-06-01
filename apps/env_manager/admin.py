from django.contrib import admin
from .models import Environment

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    # Display all fields as read-only
    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]

    # Disable the ability to add new instances
    def has_add_permission(self, request):
        return False