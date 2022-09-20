# python manage.py telbot

from datetime import time, datetime
from .models import Telegram
from account.models import Account
from django.db.models.signals import post_save
from website import settings
import requests
from board.models import Board
from django.http.request import QueryDict
from board.filters import OrderFilter
from board.models import Board, Rubric, City, Region, Age
import random
from aiogram import types
from asgiref.sync import sync_to_async

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import threading

@login_required(login_url='/login/')
def get_unique_code(request):
    account_obj = Account.objects.get(email=request.user)
    unique_code = account_obj.unique_code

    return HttpResponseRedirect("https://telegram.me/teenwork_bot?start={}".format(unique_code))


def telegram_new_ad(instance):
    board_qs = Board.objects.filter(pk=instance.pk) # filter django-filters воспринимает, а get - нет
    telegram_obj = Telegram.objects.filter(Q(telegram=True), Q(chat_id=None))

    for teleg in telegram_obj:
        rubric = teleg.rubric
        age = teleg.age
        region = teleg.region
        city = teleg.city


        if rubric == None:
            rubric = ''
        else:
            rubric = Rubric.objects.get(name=rubric).pk
        if age == None:
            age = ''
        elif age != None and instance.age == None: # если поле возраста в публик. пустое, то это все возраста. если у человека возраст какое-то число, то все возраста ему подходят
            age = ''
        else:
            age = Age.objects.get(name=age).pk
        if region == None:
            region = ''
        else:
            region = Region.objects.get(name=region).pk
        if city == None:
            city = ''
        else:
            city = City.objects.get(name=city).pk


        qdict = QueryDict(f'title_content=&price_min=&price_max=&age={age}&region={region}&city={city}&rubric={rubric}') # для того, чтобы мы могли через OrderFilter (django-filters) искать нужны Board`ы
        search = OrderFilter(qdict, queryset=board_qs)

        if search.qs:
            sync_to_async(telegram_send(teleg.chat_id, instance))
            # threading.Thread(target=telegram_send, args=(teleg.chat_id, instance), kwargs={})


def telegram_send(chat_id, instance):
    BOT_TOKEN = settings.TOKEN
    
    if instance.age != None:
        age = str(instance.age) + ' рок.'
    else:
        age = 'Усi вiки'
    
    emojis_list = ['😁','😌','🙃','😋','😏','☺️','🤫','😊','🤔','👍','👌','😀', '🤟','🤝','🙌','✊','👇','✍️']
    parse_message = f'''З`явилося нове оголошення: {random.choice(emojis_list)}:
<strong>Назва:</strong> {instance.title}
<strong>Оплата:</strong> {instance.price} {instance.currency}
<strong>Вік:</strong> {age}
<strong>Тип зайнятості:</strong> {instance.rubric}
--------------------------------------------------
<strong>Автор:</strong> {instance.author_name}
<strong>Номер телефону:</strong> {instance.phone_number}
<strong>Email:</strong> {instance.email}
    '''
    keyboard_markup = types.InlineKeyboardMarkup()
    press_btn = types.InlineKeyboardButton('Переглянути оголошення', url=f"https://teenwork.com.ua/ad/{instance.slug}")
    keyboard_markup.row(press_btn)

    # requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={parse_message}&reply_markup={open_tp}&parse_mode=HTML")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={parse_message}&parse_mode=HTML&reply_markup={keyboard_markup}")


def ad_created(chat_id, instance):
    BOT_TOKEN = settings.TOKEN
    
    parse_message = f'''Новое объявление, проверь-ка :) :
<strong>Название:</strong> {instance.title}
https://teenwork.com.ua/teenwork_admin_page_secret/board/board/{instance.pk}/change/
    '''

    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={parse_message}&parse_mode=HTML")
    # async with aiohttp.ClientSession() as session:
        
        # async with session.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={parse_message}&parse_mode=HTML") as res:
        #     

        
def ad_edited(chat_id, instance):
    BOT_TOKEN = settings.TOKEN
    
    parse_message = f'''Изменили объявление :
<strong>Название:</strong> {instance.title}
https://teenwork.com.ua/teenwork_admin_page_secret/board/board/{instance.pk}/change/
    '''

    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={parse_message}&parse_mode=HTML")


def created_post(sender, instance, created, **kwargs):
    if created == True:
        sync_to_async(ad_created(505309520,instance), thread_sensitive=True)
        # threading.Thread(target=ad_created, args=(505309520,instance))
        # ad_created(505309520,instance)
        # pass

    if created==False and instance.status == 'published' or instance.status == '24hour':
        if instance.status == '24hour':
            instance.published = datetime.now()
        telegram_new_ad(instance)

    if created==False and instance.status == 'edited':
        sync_to_async(ad_edited(505309520,instance), thread_sensitive=True)

post_save.connect(created_post, sender=Board) # этой строкой мы получаем сигнал о том, что пост был создан