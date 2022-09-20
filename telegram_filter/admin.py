from django.contrib import admin
from .models import Telegram

class TelegramAdmin(admin.ModelAdmin): 
    list_display=('person', 'telegram', 'rubric', 'age', 'region', 'city')
    list_display_links=('person',)
    readonly_fields = ('chat_id',)

admin.site.register(Telegram, TelegramAdmin)