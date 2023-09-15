from django.contrib import admin
from .models import Contact, Message, Unique_room, VerificationUser
from django.utils.html import format_html

admin.site.register(Contact)
admin.site.register(Unique_room)
admin.site.register(VerificationUser)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id_url', 'text', 'owner_id', 'sent_id', 'time_created')

    def id_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.id)
