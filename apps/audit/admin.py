from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "action", "user", "ip_address")
    list_filter = ("action", "timestamp")
    search_fields = ("user__email",)
    readonly_fields = ("user", "action", "ip_address", "user_agent", "timestamp", "details")
    date_hierarchy = "timestamp"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
