from django.contrib import admin
from account.models import Account, SocialNets, TeenworkBlog, Mailing
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


class SocialNetsAdmin(admin.ModelAdmin): # класс-редактор представления модели
    list_display=('title',)
    list_display_links=('title',) 
    fields = ('image_tag', 'title', 'img_src' ,'email_content', 'instagram_link', 'facebook_link', 'published', 'is_published' )
    search_fields=('title',)
    readonly_fields = ('published', 'image_tag')

    
    change_form_template = "others/social_nets_btns.html"


    def response_change(self, request, obj):
        if "send_email_btn" in request.POST:
            if obj.is_published == True:
                self.message_user(request, 'Эта публикая была уже отправлена')
                return redirect(f"/teenwork_admin_page_secret/account/socialnets/{obj.pk}/change")
                
            # for user in Account.objects.filter(email_subscription = True):
            #     send_email(request, user, obj)
            
            from django.core.mail import get_connection
            connection = get_connection(host='smtp.beget.com', 
                                        port=465, 
                                        username='blog@teenwork.com.ua', 
                                        password='', 
                                        use_ssl=True,
                                        fail_silently=False) 
            users = []
            for user in Account.objects.filter(Q(email_subscription = True), Q(is_active=True)):
                users.append(user)
            send_email(request, users, obj, connection)
            
            connection.close()

            obj.is_published = True
            obj.save()
            self.message_user(request, f'Опубликована запись "{obj.title}"')
            
            return redirect(f"/teenwork_admin_page_secret/account/socialnets/")
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj_title = obj.title
            obj.delete()
            self.message_user(request, f'Удалена публикация "{obj_title}"')
            if SocialNets.objects.filter(pk = next_obj).exists():
                return redirect(f"/teenwork_admin_page_secret/account/socialnets/{SocialNets.objects.get(pk = (next_obj)).pk}/change")
            else:
                return redirect('/teenwork_admin_page_secret/account/socialnets/')
        elif "send_test_email_btn" in request.POST:
            from django.core.mail import get_connection
            connection = get_connection(host='smtp.beget.com', 
                                        port=465, 
                                        username='blog@teenwork.com.ua', 
                                        password='', 
                                        use_ssl=True,
                                        fail_silently=False) 
            users = []
            if Account.objects.filter(email='buslovdmitrij0@gmail.com').exists():
                users.append(Account.objects.get(email='buslovdmitrij0@gmail.com'))
            if Account.objects.filter(email='teenworkua@gmail.com').exists():
                users.append(Account.objects.get(email='teenworkua@gmail.com'))
                
            send_email(request, users, obj, connection)
            
            connection.close()
            # send_email(request, user, obj)
            return redirect(f"/teenwork_admin_page_secret/account/socialnets/{obj.pk}/change")
        else:
            return redirect('/teenwork_admin_page_secret/account/socialnets/')



class TeenworkBlogAdmin(admin.ModelAdmin): # класс-редактор представления модели
    list_display=('title_ru', 'views',)
    list_display_links=('title_ru',) 
    fields = ('image_tag', 'title_ru', 'title_uk', 'slug', 'img_src' ,'post_content_ru', 'post_content_uk', 'published', 'views', 'status')
    search_fields=('title_ru',)
    readonly_fields = ('published', 'image_tag')
    prepopulated_fields = {'slug': ('title_ru',)} # slug применяет значение title

    
    change_form_template = "others/teenwork_blog_btns.html"

    def response_change(self, request, obj):
        if "publish_btn" in request.POST:
            if obj.status == 'published':
                self.message_user(request, 'Эта запись была уже опубликована')
                return redirect(f"/teenwork_admin_page_secret/account/teenworkblog/{obj.pk}/change")
                
            obj.status = 'published'
            obj.save()
            self.message_user(request, f'Опубликована запись "{obj.title_ru}"')
            
            return redirect(f"/teenwork_admin_page_secret/account/teenworkblog/")
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj_title = obj.title_ru
            obj.delete()
            self.message_user(request, f'Удалена запись "{obj_title}"')
            if SocialNets.objects.filter(pk = next_obj).exists():
                return redirect(f"/teenwork_admin_page_secret/account/teenworkblog/{TeenworkBlog.objects.get(pk = (next_obj)).pk}/change")
            else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/account/teenworkblog/')
        else:
            return redirect('/teenwork_admin_page_secret/account/teenworkblog/')


def mailing_start(request, users, obj, connection):
    messages = []
    for user in users:
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
        domain = get_current_site(request).domain
        link = reverse('account:unsubscribe', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
    
        activate_url='https://' + domain + link
        post_image = 'https://' + domain + '/' + str(obj.img_src)
        # post_image = 'https://teenwork.com.ua/' + str(obj.img_src)
        mail_title = obj.title + ' - Teenwork'
        variables = {
            'title':obj.title,
            'img_src': post_image,
            'email_content':obj.content,
            'activate_url': activate_url,
        }
        html = get_template('others/teenwork_mailing_email.html').render(variables)
        text = f'https://teenwork.com.ua/static/img/icons/teenwork.png - ( наше лого :) ) \n {obj.title} \n{post_image}\n{obj.content}\nЯкщо Ви не бажаєте отримувати листи, Ви можете відмовитись від розсилки {activate_url} \nTeenwork - платформа, де підлітки і не тільки можуть знайти роботу, яка їм до вподоби.'
        
        message = EmailMultiAlternatives(mail_title, text, 'help@teenwork.com.ua', [user.email])
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    
    connection.send_messages(messages)
    
from django.core.mail import get_connection
class MailingAdmin(admin.ModelAdmin): # класс-редактор представления модели
    list_display=('title',)
    list_display_links=('title',) 
    fields = ('image_tag', 'title', 'img_src' ,'content', 'published')
    search_fields=('title',)
    readonly_fields = ('published', 'image_tag')

    
    change_form_template = "others/teenwork_mailing_btns.html"

    def response_change(self, request, obj):
        if "send_email_btn" in request.POST:           
            connection = get_connection(host='smtp.beget.com', 
                                        port=465, 
                                        username='help@teenwork.com.ua', 
                                        password='Teenwork2000!', 
                                        use_ssl=True,
                                        fail_silently=False) 
            users = []
            for user in Account.objects.filter(email_subscription = True):
                users.append(user)
            mailing_start(request, users, obj, connection)
            
            connection.close()

            self.message_user(request, f'Отправлено письмо "{obj.title}"')
            
            return redirect(f"/teenwork_admin_page_secret/account/mailing/")
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj_title = obj.title
            obj.delete()
            self.message_user(request, f'Удалено письмо "{obj_title}"')
            if MailingAdmin.objects.filter(pk = next_obj).exists():
                return redirect(f"/teenwork_admin_page_secret/account/mailing/{MailingAdmin.objects.get(pk = (next_obj)).pk}/change")
            else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/account/mailing/')
        elif "send_test_email_btn" in request.POST:
            connection = get_connection(host='smtp.beget.com', 
                                        port=465, 
                                        username='help@teenwork.com.ua', 
                                        password='Teenwork2000!', 
                                        use_ssl=True,
                                        fail_silently=False) 
            user = Account.objects.get(email='buslovdmitrij0@gmail.com')
            mailing_start(request, [user], obj, connection)
            return redirect(f"/teenwork_admin_page_secretmin/account/mailing/{obj.pk}/change")
        else:
            return redirect('/teenwork_admin_page_secret/account/mailing/')



admin.site.register(Account, AccountAdmin)
admin.site.register(SocialNets, SocialNetsAdmin)
admin.site.register(TeenworkBlog, TeenworkBlogAdmin)
admin.site.register(Mailing, MailingAdmin)