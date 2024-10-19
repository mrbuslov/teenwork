from django.shortcuts import render
from board.models import Board
from account.models import Account
from board.models import TeenworkBlog
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.conf import settings
from django.db.models import Q

from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
import re
from .forms import ProfileEditForm
from telegram_filter.models import Telegram
from telegram_filter.forms import TelegramForm
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template


import threading
# view для того, чтобы быстрее отправлять email
class EmailThreading(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()



@login_required(login_url='/login/')
def profile(request):
    board_obj = Board.objects.filter(author=request.user) 
    time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
    time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

    context={
        'board_obj':board_obj,
        'time_now1':time_now1,
        'time_now2':time_now2,
    }

    return render(request, 'user/profile.html', context)

def account(request, username):
    if Account.objects.filter(username=username).exists():
        board_obj = Board.objects.filter(Q(author=Account.objects.get(username=username).pk), Q(status='published')|Q(status='24hour'))
        user = Account.objects.get(username=username)
        time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
        time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

        context={
            'board_obj':board_obj,
            'requested_user':user,
            'time_now1':time_now1,
            'time_now2':time_now2,
        }

        if user == request.user:
            return redirect('/profile/')


        return render(request, 'user/account.html', context)
    else:
        return HttpResponse('Такий Юзер зник о_о')


@login_required(login_url='/login/')
@csrf_exempt 
def profile_edit(request):
    username = request.user.username
    account = Account.objects.get(username=username)
    tlg_obj = Telegram.objects.get(person=request.user)
    tlg_form = TelegramForm(instance=tlg_obj)
    form = ProfileEditForm(instance=account)
    if request.method == 'POST' and 'profile_edit_btn' in request.POST:
        form = ProfileEditForm(request.POST, instance=account)
        if form.is_valid():
            post = form.save(commit=False)
            if request.FILES.get('img'):
                post.image = request.FILES.get('img')
            post.save()
        return redirect('account:profile_edit')

    if request.method =='POST' and 'tlg_btn' in request.POST:
        tlg_form = TelegramForm(request.POST, instance=tlg_obj)
        if tlg_form.is_valid():
            tel = tlg_form.save(commit=False)
            tel.person = request.user
            tlg_form.save()
            return redirect('account:profile_edit')
        else:  
            return redirect('account:profile_edit')
            
    if request.method == 'POST' and 'delete_account_btn' in request.POST:
        for board_obj in Board.objects.filter(author=request.user):
            board_obj.delete() # чтобы в Deleted Ads сохранить его опублик.объявл.
        Account.objects.get(id=request.user.id).delete()
        return redirect('board:index')

    elif request.method == 'POST':
        data = request.POST.get('data', None)
        isTelegram = request.POST.get('isTelegram', None)

        tel = Telegram.objects.get(person=request.user)
        if data:
            if data == 'checked':
                tel.telegram = True
                data = 'true'
            else:
                tel.telegram = False
                data = 'false'
            tel.save()
            return JsonResponse(data, safe=False)
        elif isTelegram:
            if tel.telegram == True:
                isTelegram = 'true'
            else:
                isTelegram = 'false'
            return JsonResponse(isTelegram, safe=False)

    return render(request, 'user/profile_edit.html', {'form':form, 'account':account, 'tlg_form':tlg_form,})




def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if request.method == 'POST':
            data=''
            username_check = request.POST.get('username', None)
            email_check = request.POST.get('email', None)
            phone_number_check = request.POST.get('phone_num', None)

            if username_check:
                if Account.objects.filter(username=username_check.lower()).exists():
                    data='username_taken'
                else:
                    data='username_free'
            elif email_check:
                if Account.objects.filter(email=email_check.lower()).exists():
                    data='email_taken'
                else:
                    data='emil_free'
            elif phone_number_check:
                if Account.objects.filter(phone_number=phone_number_check).exists():
                    data='phone_taken'
                else:
                    data='phone_free'


            return JsonResponse(data, safe=False)
        
        if Account.objects.filter(username=username.lower()).exists() or Account.objects.filter(email=email.lower()).exists() or Account.objects.filter(phone_number=phone_number).exists():
            return redirect('account:registration')
            
        if re.match("^[a-z0-9_]+$", username.lower()) == None:
            return redirect('account:registration')

        user = Account.objects.create_user(username=username.lower(), password=password, email=email.lower(), phone_number=phone_number)
        user.is_active = False # Меняем на True после регистрации
        user.save()

        tlg_user = Telegram.objects.create(person=user)
        tlg_user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        domain = get_current_site(request).domain
        link = reverse('account:activate', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

        activate_url='https://' + domain + link

        # email_context = {
        #     'user':user,
        #     'activate_url': activate_url,
        # }

        # email_subject = 'Активация профиля'
        # # email_body = 'Здравствуй, ' + user.username + '! Используйте эту ссылку, чтобы подтвердить Ваш аккаунт\n' + activate_url # email_body = render_to_string('registration/email.html')
        # email_body = render_to_string('registration/email.html', email_context)
        # email_msg = EmailMessage(
        #     email_subject,
        #     email_body,
        #     settings.EMAIL_HOST_USER,
        #     [email],
        # )

        # # email_msg.send(fail_silently=False) 

        # EmailThreading(email_msg).start()








        mail_title = "Активація"
        variables = {
            'activate_url': activate_url,
            'watch_here': 'https://' + domain + '/rules/',
        }
        html = get_template('registration/email.html').render(variables)
        text = f'https://teenwork.com.ua/static/img/icons/teenwork.png - ( наше лого :) )\nДавайте підтвердимо Ваш аккаунт\nЩоб почати користуватися Teenwork, просто натисніть кнопку підтвердження адреси електронної пошти нижче:\nПідтвердити\n{activate_url}\nУ вас є питання? Подивіться тут.\nhttps://teenwork.com.ua/rules/\nTeenwork - платформа, де підлітки і не тільки можуть знайти роботу, яка їм до вподоби.'
        
        msg = EmailMultiAlternatives(
            mail_title,
            text,
            settings.EMAIL_HOST_USER,
            [email])
        msg.attach_alternative(html, "text/html")
        # msg.send(fail_silently=False) 
        EmailThreading(msg).start()
        

        return render(request, 'registration/registration_success.html')
    else:
        return render(request, 'registration/registration.html')

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = Account.objects.get(email=email)

        uidb64 =urlsafe_base64_encode(force_bytes(user.pk))

        domain = get_current_site(request).domain
        link = reverse('account:activate', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

        activate_url='https://' + domain + link


        mail_title = "Активація"
        variables = {
            'activate_url': activate_url,
            'watch_here': 'https://' + domain + '/rules/',
        }
        html = get_template('registration/email.html').render(variables)
        text = get_template('registration/email.html').render(variables)
        
        msg = EmailMultiAlternatives(
            mail_title,
            text,
            settings.EMAIL_HOST_USER,
            [email])
        msg.attach_alternative(html, "text/html")
        EmailThreading(msg).start()
        

        return render(request, 'registration/resend_activation_email_success.html')
    else:
        return render(request, 'registration/resend_activation_email.html')




from django.views.generic import View
class VerificationView(View):
    def get(self,request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as e:
            user = None
        
        if user is not None:
            if not token_generator.check_token(user,token):
                return redirect('account:login')


            if user.is_active:
                return redirect('account:login')
            user.is_active = True
            user.save()

            return redirect('account:login')
        else:
            raise Exception


def user_login(request):
    if request.user.is_authenticated:
        return redirect('board:index')
    else:
        if request.method == 'POST':

            if request.POST.get('email_login', None):
                data=''
                email_check = request.POST.get('email_login', None)

                if email_check:
                    if Account.objects.filter(email=email_check.lower()).exists():
                        if Account.objects.get(email=email_check.lower()).is_active == False:
                            data='not_active'
                        if Account.objects.get(email=email_check.lower()).is_blocked == True:
                            data='blocked'
                    elif Account.objects.filter(phone_number=email_check).exists():
                        if Account.objects.get(phone_number=email_check).is_active == False:
                            data='not_active'
                        if Account.objects.get(phone_number=email_check).is_blocked == True:
                            data='blocked'
                    elif Account.objects.filter(username=email_check.lower()).exists():
                        if Account.objects.get(username=email_check.lower()).is_active == False:
                            data='not_active'
                        if Account.objects.get(username=email_check.lower()).is_blocked == True:
                            data='blocked'
                    else:
                        data='not_exists'

                return JsonResponse(data, safe=False)

            username = request.POST.get('username')
            password = request.POST.get('password')

            continue_execution = True
            try:
                user = authenticate(username=Account.objects.get(username=username.lower()).email, password=password)
                continue_execution = False
            except:
                pass
            if continue_execution:
                try:
                    # номер телефона
                    user = authenticate(username=Account.objects.get(phone_number=username).email, password=password)
                except:
                    # email
                    user = authenticate(email=username.lower(), password=password)
                

            if user is not None:
                if user.is_blocked:
                    return redirect('account:logout')
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('board:index')
            else:  
                return render(request, 'registration/login.html')
        else:  
            return render(request, 'registration/login.html')
def user_logout(request):
    logout(request)
    return redirect('board:index')


from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
class PasswordResetPSWRDView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')





@csrf_exempt
@login_required(login_url='/login/', redirect_field_name='/') # redirect_field_name - чтобы просто перенаправило на  главную, а не на ту же страницу
def favourite_add(request, pk):
    pk = int(pk)
    if request.user.is_authenticated:
        post = get_object_or_404(Board, id=pk)
        if post.favourites.filter(id=request.user.pk).exists():
            post.favourites.remove(request.user)
        else:
            post.favourites.add(request.user)

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # else:
    #     return redirect('/login/')

@csrf_exempt
@login_required(login_url='/login/')
def favourite_list(request):
    new = Board.objects.filter(favourites=request.user)

    time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
    time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

    context = {
        'new':new,
        'time_now1':time_now1,
        'time_now2':time_now2,
    }

    return render(request, 'board/favourites.html', context)




class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'registration/reset_email.html')
    
    def post(self, request):
        email = request.POST.get('email', None)
        
        if email is None:
            # messages.error(request, 'Не забудьте вписать email')
            return render(request, 'registration/reset_email.html')

        user = Account.objects.filter(email=email)
        if user.exists():
            uidb64 =urlsafe_base64_encode(force_bytes(user[0].pk))

            domain = get_current_site(request).domain
            link = reverse('account:set_new_pswrd', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user[0])})

            activate_url='https://' + domain + link

            # email_context = {
            #     'user':user,
            #     'activate_url': activate_url,
            # }

            # email_subject = 'Обновление пароля'
            # # email_body = 'Здравствуй, ' + user.username + '! Используйте эту ссылку, чтобы подтвердить Ваш аккаунт\n' + activate_url # email_body = render_to_string('registration/email.html')
            # email_body = render_to_string('registration/reset_password.html', email_context)
            # email_msg = EmailMessage(
            #     email_subject,
            #     email_body,
            #     settings.EMAIL_HOST_USER,
            #     [email],
            # )

            # # email_msg.send(fail_silently=False) 


            # EmailThreading(email_msg).start() # мы быстрее отправляем email





            mail_title = "Оновлення пароля"
            variables = {
                'activate_url': activate_url,
            }
            html = get_template('registration/reset_password.html').render(variables)
            text = f'https://teenwork.com.ua/static/img/icons/teenwork.png - ( наше лого :) )\nЗабули пароль?\nЩоб скинути пароль, натисніть кнопку нижче.\nСкинути\n{activate_url}\nЯкщо Ви не бажаєте змінювати свій пароль або не запитували скидання паролю, Ви можете проігнорувати або видалити цей лист.\nTeenwork - платформа, де підлітки і не тільки можуть знайти роботу, яка їм до вподоби.'
            
            msg = EmailMultiAlternatives(
                mail_title,
                text,
                settings.EMAIL_HOST_USER,
                [email])
            msg.attach_alternative(html, "text/html")
            # msg.send(fail_silently=False) 
            EmailThreading(msg).start() # мы быстрее отправляем email


            return render(request, 'registration/reset_email_success.html')
        else:
            return redirect('/registration/')
        
    
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.utils.html import strip_tags
from django.utils.translation import get_language
class SetNewPswrdView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = Account.objects.get(pk=user_id)

            if PasswordResetTokenGenerator().check_token(user, token):
                # Пароль кликают 2-ой раз, так нельзя. Отошлём на повторную отправку
                return render(request, 'registration/reset_email.html')
        except DjangoUnicodeDecodeError as identifier:
            return render(request, 'registration/reset_email.html')
        return render(request, 'registration/set_new_pswrd.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        password = request.POST.get('password', None)
        if password is None or len(password) < 4 or len(password) > 20:
            return render(request, 'registration/set_new_pswrd.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = Account.objects.get(pk=user_id)
            user.set_password(password)
            user.is_active = True
            user.save()

            return redirect('/login/')
        except DjangoUnicodeDecodeError as identifier:
            return render(request, 'registration/set_new_pswrd.html', context)


class UnsubscribeView(View):
    def get(self,request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except Exception as e:
            user = None
        
        if user is not None:
            if not token_generator.check_token(user,token):
                return render(request, 'others/user_unsubscribed.html')


            if user.email_subscription == False:
                return render(request, 'others/user_unsubscribed.html')
            user.email_subscription = False
            user.save()

            return render(request, 'others/user_unsubscribed.html')
        else:
            raise Exception
            
            
