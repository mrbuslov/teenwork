import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# python-telegram-bot
# python manage.py telbot
from django.core.management.base import BaseCommand
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from website import settings
from telegram_filter.models import Telegram

from asgiref.sync import sync_to_async
import logging
from account.models import Account
import aiohttp
from aiogram.utils.markdown import bold, code, italic, text
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text

@sync_to_async
def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None

@sync_to_async
def get_account(unique_code):
    if Account.objects.filter(unique_code=unique_code).exists():
        return Account.objects.get(unique_code=unique_code)
    else:
        return None
@sync_to_async
def get_telegram(account_obj):
    return Telegram.objects.get(person=account_obj)


GET_IP_URL = 'http://bot.whatismyipaddress.com/'


from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1 = KeyboardButton('Что бот может делать?🤖')
button2 = InlineKeyboardButton('Изменить предпочтения🤔', url="https://teenwork.com.ua/profile_edit/?telegram")

markup = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2)


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN)
        dp = Dispatcher(bot)

        @dp.message_handler(commands=['start'])
        async def process_start_command(message: types.Message):
            await types.ChatActions.typing() # "Бот печатает ..."

            unique_code = await extract_unique_code(message.text)
            if unique_code and await get_account(unique_code):
                account_obj = await get_account(unique_code)
                telegram_obj = await get_telegram(account_obj)

                telegram_obj.chat_id = message.chat.id
                telegram_obj.save()

                first_name = message.from_user.first_name
                account_first_name = account_obj.first_name
                username = account_obj.username
                
                try:
                    if first_name:
                        reply = "Здрастуйте, {0}!".format(first_name)
                    elif account_first_name:
                        reply = "Здрастуйте, {0}!".format(account_first_name)
                    elif username:
                        reply = "Здрастуйте, {0}!".format(username)
                    else:
                        reply = "Здрастуйте!"
                except:
                    reply = "Здрастуйте!"

                if telegram_obj.telegram == False:
                    reply += '\nМи надсилатимемо Вам цікаві вакансії.\nЩоб ми знали, що краще Вам пропонувати, заповніть форму на нашому сайті'

                    keyboard_markup = types.InlineKeyboardMarkup()
                    press_btn = types.InlineKeyboardButton('Перейти до форми', url="https://teenwork.com.ua/profile_edit/?telegram")
                    keyboard_markup.row(press_btn)
                    
                    await bot.send_message(message.from_user.id, reply, reply_markup=keyboard_markup)
                else:
                    await bot.send_message(message.from_user.id, reply, reply_markup=markup)

            else:
                reply = "Щоб ми могли знати Ваші уподобання, зайдіть у бота через наш сайт"
                
                keyboard_markup = types.InlineKeyboardMarkup()
                press_btn = types.InlineKeyboardButton('Зайти на сайт', url="https://teenwork.com.ua/telegram_bot")
                keyboard_markup.row(press_btn)
                    
                await bot.send_message(message.from_user.id, reply, reply_markup=keyboard_markup)



        @dp.message_handler(commands=['help'])
        async def process_help_command(message: types.Message):
            await types.ChatActions.typing() # "Бот печатает ..."

            msg = []
            msg.append(text("   Хочете запитати, що вміє цей бот? Якщо коротко, то надсилати хороші вакансії по Вашим", italic("уподобанням"),":relaxed:"))
            msg.append(text("   Якщо докладніше, то ми порівнюємо кожне оголошення з тим, що Ви написали у формі знизу, а після цього, якщо воно відповідає Вашим вимогам, відправляємо", italic("повідомлення")," про нього Вам."))
            msg.append(text("   Тут головне швидкість - чим швидше Ви відгукнулися на оголошення, тим швидше Ви отримали цікаву роботу, вірно?)\n Для цього ми працюємо з Вами через цей бот",':grin:'))

            keyboard_markup = types.InlineKeyboardMarkup()
            press_btn = types.InlineKeyboardButton('Перейти до форми', url="https://teenwork.com.ua/profile_edit/?telegram")
            keyboard_markup.row(press_btn)
            
            await bot.send_message(message.chat.id, emojize(text(*msg, sep='\n')), parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_markup)


        @dp.message_handler()
        async def send_back(message: types.Message):
            if str(message.text).lower() == 'привет' or str(message.text).lower() == 'привіт':
                await bot.send_message(message.chat.id, 'Привіт!) У мене є багато команд, із чого почнемо?', reply_markup=markup)
            if str(message.text).lower() == 'что бот может делать?🤖' or str(message.text).lower() =='що бот може робити?🤖':
                await process_help_command(message)
            if str(message.text).lower() == 'изменить предпочтения🤔' or str(message.text).lower() == 'змінити вподобання🤔':
                keyboard_markup = types.InlineKeyboardMarkup()
                press_btn = types.InlineKeyboardButton('Змінити уподобання', url="https://teenwork.com.ua/profile_edit/?telegram")
                keyboard_markup.row(press_btn)
                
                await bot.send_message(message.chat.id, 'Так, давайте спробуємо щось нове', reply_markup=keyboard_markup)
   

        executor.start_polling(dp)