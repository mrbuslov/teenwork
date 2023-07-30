from django.contrib import admin
from account.models import Account
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q


class HidePassword(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('password',)



from django.db.models import Q
class ask_user_to_activate(admin.SimpleListFilter):
    title = 'Неактивные пользователи'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Активный'),
            ('not_activated', 'Не активный'), # если поменять название, то меняй второй параметр
            ('not_activated_and_not_asked', 'Не активный и не спрошенный'), # если поменять название, то меняй второй параметр
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'not_activated':
            return queryset.filter(is_active = False)
        if self.value().lower() == 'activated':
            return queryset.filter(is_active = True)
        if self.value().lower() == 'not_activated_and_not_asked':
            return queryset.filter(Q(is_active = False), Q(is_asked_for_activ = False))

class AccountAdmin(UserAdmin): 
    form = HidePassword # скрываем пароль

    list_display = ('email', 'username', 'person_age')
    list_filter = ('email_subscription', ask_user_to_activate,)
    search_fields = ('email','username')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ( 'image', 'username', 'phone_number', 'first_name', 'last_name', 'person_age', 'unique_code', 'date_joined','last_login', 'email_subscription')}),
        ('Разрешения', {'fields': ('is_admin','is_active', 'is_blocked', 'is_staff', 'is_superuser', 'is_official', 'is_asked_for_activ', 'groups', 'user_permissions',)}),
    )
    
    # если захотим добавить аккаунт со страницы admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password',),
        }),
    )

    readonly_fields = ('person_age', 'unique_code', 'date_joined','last_login')
    # filter_horizontal = ('groups', 'user_permissions',)

    class Meta:
        model = Account


import threading
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from website import settings
from django.template.loader import get_template

# view для того, чтобы быстрее отправлять email
# class EmailThreading(threading.Thread):
#     def __init__(self, email_message):
#         self.email_message = email_message
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email_message.send()
def send_email(request, users, obj, connection):
    messages = []
    for user in users:
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
        domain = get_current_site(request).domain
        link = reverse('account:unsubscribe', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
    
        activate_url='https://' + domain + link
        post_image = 'https://' + domain + '/' + str(obj.img_src)
        mail_title = obj.title + ' - Teenwork'
        variables = {
            'title':obj.title,
            'img_src': post_image,
            'email_content':obj.email_content,
            'instagram_link':obj.instagram_link,
            'facebook_link':obj.facebook_link,
            'activate_url': activate_url,
        }
        html = get_template('others/social_nets_email.html').render(variables)
        text = f'https://teenwork.com.ua/static/img/icons/teenwork.png - ( наше лого :) ) \n {obj.title} \n{post_image}\n{obj.email_content}\nInstagram:{obj.instagram_link}\nFacebook:{obj.facebook_link}\nЯкщо Ви вже підписалися на наші соц.мережі, Ви можете відмовитись від розсилки {activate_url} \nTeenwork - платформа, де підлітки і не тільки можуть знайти роботу, яка їм до вподоби.'
        
        # msg = EmailMultiAlternatives(
        #     mail_title,
        #     text,
        #     settings.EMAIL_HOST_USER,
        #     [user.email])
        # msg.attach_alternative(html, "text/html") 
        # EmailThreading(msg).start()
        message = EmailMultiAlternatives(mail_title, text, 'blog@teenwork.com.ua', [user.email])
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    
        # EmailThreading(message).start()
    connection.send_messages(messages)


admin.site.register(Account, AccountAdmin)