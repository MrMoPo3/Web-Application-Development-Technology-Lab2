from django.contrib import admin

from .models import OnlineUser


@admin.register(OnlineUser)
class OnlineUserAdmin(admin.ModelAdmin):
    list_display = ("user", "channel_name", "connected_at", "last_seen")
    search_fields = ("user__email", "user__name")
    readonly_fields = ("connected_at", "last_seen")
