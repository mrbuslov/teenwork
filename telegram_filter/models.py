from django.db import models
from account.models import Account

class Telegram(models.Model):
    telegram = models.BooleanField(null=True, default=False, verbose_name='Telegram')

    rubric=models.ForeignKey('board.Rubric',null=True, on_delete=models.PROTECT,verbose_name='Рубрика', blank=True)
    age = models.ForeignKey('board.Age',null=True, on_delete=models.PROTECT,verbose_name='Возраст', blank=True)
    region = models.ForeignKey('board.Region', null=True, on_delete=models.PROTECT, verbose_name='Область', blank=True)
    city = models.ForeignKey('board.City', null=True, on_delete=models.PROTECT,  verbose_name='Город', blank=True)

    person = models.ForeignKey('account.Account',null=True, on_delete=models.CASCADE, verbose_name='Человек', blank=True)
    chat_id = models.BigIntegerField(null=True, blank=True, verbose_name='chat id', editable=False)
    
    class Meta:
        verbose_name_plural='Telegram Users' 
        verbose_name= 'Telegram'
        ordering=['telegram']

    # нужно, чтобы мы могли видеть нормальный путь к объекту в /admin ( Начало-> Telegram Filter -> ...)
    def __str__(self):
        return f'{self.person} #{self.chat_id}'
        
    def save(self,  *args, **kwargs):
        if self.person.person_age == None and self.age != None:
            user = Account.objects.get(email=self.person)
            user.person_age = self.age
            user.save()
    
        super(Telegram, self).save(*args, **kwargs)