from django.db import models
from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length = 500, verbose_name='Чат')
    ad_fk = models.ForeignKey('board.Board', on_delete=models.CASCADE, verbose_name='Объявление №', default=None, null=True)
    participants = models.ManyToManyField('account.Account', related_name="participants", default=None, blank=True, verbose_name = "Участники чата")

class Message(models.Model):
    value = models.CharField(max_length = 10000, verbose_name='Сообщение')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Чат №')
    date = models.DateTimeField(default = datetime.now, blank = True, verbose_name='Дата отправки')
    sender = models.ForeignKey('account.Account', on_delete=models.SET_NULL, verbose_name='Отправитель', null=True)

    class Meta:
        get_latest_by = 'id' # Это нам нужно для того, чтобы мы могли получить последний опубликованный объект в views.py через .latest()