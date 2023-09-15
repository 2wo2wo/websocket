from django.contrib import admin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id_url", "email", "last_name", "first_name")

    def id_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.id)
