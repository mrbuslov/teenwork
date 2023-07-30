from django.contrib import admin
from .models import Room, Message

class RoomAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ('name',)
class MessageAdmin(admin.ModelAdmin):
    list_display=('room', 'value', 'date', 'sender')
    search_fields = ( 'sender',)
    ordering = ['-date']

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)