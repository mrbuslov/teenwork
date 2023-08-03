import json
import locale
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.response import HttpResponse, JsonResponse
from django.utils.translation import get_language
from account.models import Account
from board.filters import OrderFilter
from board.forms import BoardForm
from board.models import Age, Board, DeletedAds, Image
from django.shortcuts import redirect, render
from django.db.models import Case, F, When, Q
from chat.views import checkview
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.http.request import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def add_advert(request, form):
    post = form.save(commit=False)
    if request.user.is_authenticated:
        post.author = request.user
        post.status = 'draft'
    else:
        post.status = '24hour_draft'

    post.save()

    photo1_id = request.POST.get('photo1_id', None)
    photo2_id = request.POST.get('photo2_id', None)
    photo3_id = request.POST.get('photo3_id', None)

    photo1_pos = request.POST.get('photo1_pos', None)
    photo2_pos = request.POST.get('photo2_pos', None)
    photo3_pos = request.POST.get('photo3_pos', None)

    print(photo1_pos, photo2_pos, photo3_pos)

    if photo1_id != 'undefined' and photo1_id != '': 
        if not Image.objects.filter(id=photo1_id).exists(): raise Exception('Пути фотографий не найдены')
    if photo2_id != 'undefined' and photo2_id != '': 
        if not Image.objects.filter(id=photo2_id).exists(): raise Exception('Пути фотографий не найдены')
    if photo3_id != 'undefined' and photo3_id != '': 
        if not Image.objects.filter(id=photo3_id).exists(): raise Exception('Пути фотографий не найдены')

    if photo1_id == 'undefined' or photo2_id == 'undefined' or photo3_id == 'undefined': raise Exception(_('Undefined - ошибка загрузки изображений'))

    try:
        if photo1_pos and photo1_id: Image.objects.filter(id = photo1_id).update(position=int(photo1_pos), board=post)
        if photo2_pos and photo2_id: Image.objects.filter(id = photo2_id).update(position=int(photo2_pos), board=post)
        if photo3_pos and photo3_id: Image.objects.filter(id = photo3_id).update(position=int(photo3_pos), board=post)
    except Exception as e: 
        print(e)
        raise Exception('Какой-то умник решил подправить данные в позиции фотографий /add/')


def add_load_image(request):
    images = request.FILES.getlist('img')
    img_list = []
    img_id_list = []
    if images:
        for index, i in enumerate(images):
            image = Image.objects.create(image=i)
            img_list.append(str(image.image.url))
            img_id_list.append(str(image.id))
    return JsonResponse({'data':img_list, 'ids':img_id_list}, status=200)


def get_user_data(request):
    phone_num = request.POST.get('phone_num', None)
    user_data = request.POST.get('user_data', None)
    
    if phone_num:
        data = ''
        if not request.session.session_key:
            board_obj = Board.objects.filter(
                Q(phone_number__icontains = phone_num)|
                # Q(email = email),
                Q(status='24hour')|Q(status='24hour_draft'),
            )
            deleted_board_obj = DeletedAds.objects.filter(
                Q(phone_number__icontains = phone_num)|
                # Q(email = email),
                Q(status='24hour')|Q(status='24hour_draft'),
            )
            count = board_obj.count() + deleted_board_obj.count()
            if count >= 2:
                data = "more_than_3"
            else:
                data = "less_than_3"
        else:
            data = "less_than_3"
        return JsonResponse(data, safe=False)

    elif user_data:
        try:
            if request.session.session_key:
                first_n = request.user.first_name
                last_n = request.user.last_name
    
                if first_n == '' and last_n == '':
                    try:
                        first_n = Board.objects.filter(author = request.user)[0].author_name
                    except:
                        first_n = request.user.username
                
                data = [first_n, last_n, request.user.phone_number, request.user.email]
            else:
                data = [None, None, None, None]
        except:
            data = [None, None, None, None]
        
        return JsonResponse(data, safe=False)


def edit_adt(request, pk):
    board = Board.objects.get(pk=pk)
    form = BoardForm(request.POST, instance=board) # instance - исправляемая запись
    if request.user == board.author:
        if request.method == 'POST':
            if form.is_valid():
                if form.has_changed():
                    post = form.save(commit=False)
                    post.status = 'edited'
                    post = form.save()

                return redirect('/profile/')

        context = get_edit_page(pk)
        return render(request, 'board/edit.html', context)
    else:
        return redirect('/profile/')

def get_edit_page(pk):
    board = Board.objects.get(pk=pk)
    form = BoardForm(instance=board)

    board_obj = Board.objects.get(pk=pk)
    photo_list = []

    context = {
        'form':form,
        'board_obj':board_obj,
        'photo_list':photo_list,
        'pk':pk,
    }
    return context


def archive_adt(request, pk):
    board = Board.objects.get(pk=pk)
    if request.user == board.author:
        if board.status == 'archive':
            board.status = 'edited'
            board.save()
        else:
            board.status = 'archive'
            board.save()
        return redirect('/profile/')
    else:
        return redirect('/')


from django.http import Http404
def show_advertisement(request,slug):
    if Board.objects.filter(slug=slug).exists():
        board_obj = Board.objects.get(slug=slug)
        Board.objects.filter(slug=slug).update(views=F('views')+1)
        is_not_author = True
        if board_obj.author == request.user or not board_obj.author:
            is_not_author = False

        time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
        time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта
        # для того, чтобы вместо дня 1 марта превратить в 01 марта

        # photo_list = []
        # if board_obj.image1 and board_obj.image1.url != '':
        #     photo_list.append(board_obj.image1.url)
        # if board_obj.image2 and board_obj.image2.url != '':
        #     photo_list.append(board_obj.image2.url)
        # if board_obj.image3 and board_obj.image3.url != '':
        #     photo_list.append(board_obj.image3.url)
        
        if request.method == 'POST':
            txtArea = request.POST.get('txtArea',None)
            if txtArea:
                return checkview(request, room=board_obj.slug, message=txtArea, board_obj=board_obj)
            else:
                txtArea = 'Здравствуйте, мне понравилась Ваша работа! '
                if request.user.first_name or request.user.last_name:
                    txtArea += f'Меня зовут {request.user.first_name} {request.user.last_name}. '
                if request.user.person_age:
                    txtArea += f'Мне {request.user.person_age} лет. '
                if request.user.phone_number:
                    txtArea += f'Я хочу поговорить с Вами о деталях работы. Мой номер: {request.user.phone_number}.'
                return checkview(request, room=board_obj.slug, message=txtArea, board_obj=board_obj)
        account = ''
        if board_obj.author:
            account = Account.objects.get(email = board_obj.author)

        context={
            'val':board_obj,
            # 'photo_list':photo_list,
            'time_now1':time_now1,
            'time_now2':time_now2,
            'is_not_author':is_not_author,
            'account':account,
        }
        

        return render(request, 'board/advertisement.html', context)
    else:
        raise Http404
        # raise Exception('qwe')


def show_index(request):
    # смотрим, если у нас один запрос, переадресовываем на страницу нормальную, не через ?title_content&...
    # mydict1 = {'title_content': [''], 'price_min': [''], 'price_max': [''], 'age': [''], 'city': [''], 'rubric': ['']}
    # mydict2 = dict(request.GET)
    # vals = [tuple(sorted(x)) for x in mydict1.values()]
    # mydict2 = {k:v for (k,v) in mydict2.items() if tuple(sorted(v)) not in vals}
    
    if request.user.is_authenticated:
        if request.user.is_blocked:
            return redirect('account:logout')


    if request.user.is_authenticated:
        if Account.objects.get(email=request.user).person_age != 0 or Account.objects.get(email=request.user).person_age != None:
            # Идея в том, чтобы сначала найти записи с возрастом пользователя, показать ему их, а потом уже другие
            person_age = Account.objects.get(email=request.user).person_age

            board_obj1 = Board.objects.filter(Q(age=person_age), Q(status='published')|Q(status='24hour')).order_by('?') # order_by('-published')
            board_obj_other = Board.objects.filter(~Q(age=person_age), Q(status='published')|Q(status='24hour')).order_by('?') # ? - рандом

            arr = []
            for val in board_obj1:
                arr.append(val.id)
            for val in board_obj_other:
                arr.append(val.id)

            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(arr)])
            board_obj = Board.objects.filter(pk__in=arr).order_by(preserved) 
        else:
            board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour')).order_by('?')
    else:
        board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour')).order_by('?')

    myFilter = OrderFilter(request.GET, queryset=board_obj)

    time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
    time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

    paginator = Paginator(myFilter.qs, 1)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # for val in Board.objects.all():
    #     print(val)
    #     if val.pk == 71:
    #         print('val')
    #         val.delete()

    # print(Board.objects.get(pk=68))

    # def get_ip(request):
    #     adress = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if adress:
    #         ip = adress.split(',')[-1].strip()
    #     else:
    #         ip = request.META.get('REMOTE_ADDR')
    #     return ip
    # ip = get_ip(request)
    # user_ip = UserIp(ip_adress = ip)
    #print(ip)
    # result = UserIp.objects.filter(Q(ip_adress__icontains=ip))
    # if len(result)==1:
    #     #print('User exists')
    #     pass
        
    # elif len(result) > 1:
    #     #print('User exists more...')
    #     pass
    # else:
    #     user_ip.email = request.user
    #     user_ip.save()
    #     #print('user is unique')
    
    # count = UserIp.objects.all().count

    context={
        'response':response,
        'myFilter':myFilter,
        # 'count':count,
        'time_now1':time_now1,
        'time_now2':time_now2,
        'age_range':Age.objects.all(),
    }

    return render(request, 'board/index.html', context)
    
    
def load_more_index_adts(request):
    adts_arr = request.POST.getlist('adts_arr[]')
    lang = request.POST.get('lang', None)
    what_user_searches = request.POST.get('what_user_searches', None)
    totalData = Board.objects.filter(Q(status='published')|Q(status='24hour')).count()

    if lang == 'uk':
        translation.activate('uk') # почему-то, когда мы делаем ajax, то язык по дефолту, поэтому нам нужно явно поменять язык
    for i, val in enumerate(adts_arr):
        adts_arr[i] = adts_arr[i].replace('/en','').replace('/ad','').replace('/','') # очищаем, чтобы получить только slug

    time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
    time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта
    if get_language() == 'uk': locale.setlocale(locale.LC_TIME, 'uk_UA.utf8') # для украинской версии отображения времени
    else: locale.setlocale(locale.LC_TIME, 'ru_RU.utf8') # для русской версии отображения времени

    # сортировка объявлений
    how_many_show = 20 # кол-во объявлений для показа на главной странице

    if what_user_searches:
        if request.user.is_authenticated:
            if Account.objects.get(email=request.user).person_age != 0 or Account.objects.get(email=request.user).person_age != None:
                person_age = Account.objects.get(email=request.user).person_age

                board_obj1 = Board.objects.filter(Q(age=person_age), Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')
                board_obj_other = Board.objects.filter(~Q(age=person_age), Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')

                arr = []
                for val in board_obj1:
                    arr.append(val.id)
                for val in board_obj_other:
                    arr.append(val.id)

                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(arr)])
                board_obj = Board.objects.filter(pk__in=arr).order_by(preserved)
                
                qdict = QueryDict(what_user_searches[1:]) # request.GET не передаётся сюда, поэтому возьмём его через js
                board_obj = OrderFilter(qdict, queryset=board_obj).qs[:how_many_show]
            else:
                board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')[:how_many_show]
        else:
            board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')
            
            qdict = QueryDict(what_user_searches[1:]) # request.GET не передаётся сюда, поэтому возьмём его через js
            board_obj = OrderFilter(qdict, queryset=board_obj).qs[:how_many_show]
    else:
        if request.user.is_authenticated:
            if Account.objects.get(email=request.user).person_age != 0 or Account.objects.get(email=request.user).person_age != None:
                person_age = Account.objects.get(email=request.user).person_age

                board_obj1 = Board.objects.filter(Q(age=person_age), Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')[:how_many_show] # чтобы не загружать абсолютно все объявления, зарузим тех и тех, чтобы уже наверняка
                board_obj_other = Board.objects.filter(~Q(age=person_age), Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')[:how_many_show]

                arr = []
                for val in board_obj1:
                    arr.append(val.id)
                for val in board_obj_other:
                    arr.append(val.id)

                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(arr)])
                board_obj = Board.objects.filter(pk__in=arr).order_by(preserved)[:how_many_show]
            else:
                board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')[:how_many_show]
        else:
            board_obj = Board.objects.filter(Q(status='published')|Q(status='24hour'), ~Q(slug__in = adts_arr)).order_by('?')[:how_many_show]

    board_obj_json=serializers.serialize('json',board_obj)
    # меняем поля, чтобы отображался не id у полей, а их имена
    info = json.loads(board_obj_json)
    counter = 0
    for i in info:
        info[counter]['fields']['adt_url'] = ''
        info[counter]['fields']['fav_url'] = ''
        info[counter]['fields']['user_url'] = ''
        info[counter]['fields']['tick_text'] = ''
        info[counter]['fields']['phone_num_name'] = ''
        info[counter]['fields']['author_official'] = False
        info[counter]['fields']['user_in_favourites'] = False
        info[counter]['fields']['adt_username'] = False

        info[counter]['fields']['image1'] = str(list(board_obj)[counter].get_image())
        if get_language() == 'en':
            info[counter]['fields']['adt_url'] = '/en/ad/'+str(list(board_obj)[counter].slug) + '/'
        else:
            info[counter]['fields']['adt_url'] = '/ad/'+str(list(board_obj)[counter].slug) + '/'
        info[counter]['fields']['currency'] = str(list(board_obj)[counter].currency)
        info[counter]['fields']['rubric'] = str(list(board_obj)[counter].rubric)
        info[counter]['fields']['city'] = str(list(board_obj)[counter].city)
        if list(board_obj)[counter].age:
            info[counter]['fields']['age'] = _('Возраст:') + ' ' +  str(list(board_obj)[counter].age) + ' ' + _('лет.')
        else:
            info[counter]['fields']['age'] = _('Возраст:') + ' ' + str(_('Все'))
        _time_board_obj = list(board_obj)[counter].published
        _time_day = str(_time_board_obj.day).zfill(2) + '.' + str(_time_board_obj.month).zfill(2) + '.' + str(_time_board_obj.date().year).zfill(2)

        _time = board_obj[counter].published
        if _time_day == time_now1:
            st = _time.strftime("%H:%M")
            info[counter]['fields']['published'] = _('Сегодня в') + ' ' + str(st)
        elif _time_day == time_now2:
            st = _time.strftime("%H:%M")
            info[counter]['fields']['published'] = _('Вчера в') + ' ' + str(st)
        else:
            st = _time.strftime("%d %b в %H:%M")
            # info[counter]['fields']['published'] = st.title().replace('В','в')
            info[counter]['fields']['published'] = str(st).replace('В','в')
        
        athr = info[counter]['fields']['author']
        if athr != '' and  Account.objects.filter(id=athr).exists():
            if Account.objects.get(id=athr).is_official:
                info[counter]['fields']['author_official'] = True
            
            if request.user in list(board_obj)[counter].favourites.all():
                info[counter]['fields']['user_in_favourites'] = True
            if get_language() == 'en':
                info[counter]['fields']['fav_url'] = '/en/fav/' + str(list(board_obj)[counter].pk) + '/'
                if str(list(board_obj)[counter].author) != '':
                    info[counter]['fields']['user_url'] = '/en/by/' + str(list(board_obj)[counter].author.username) + '/'
                else:
                    info[counter]['fields']['user_url'] = ''
            else:
                info[counter]['fields']['fav_url'] = '/fav/' + str(list(board_obj)[counter].pk) + '/'
                if str(list(board_obj)[counter].author) != '':
                    info[counter]['fields']['user_url'] = '/by/' + str(list(board_obj)[counter].author.username) + '/'
                else:
                    info[counter]['fields']['user_url'] = ''

        info[counter]['fields']['adt_username'] = str(list(board_obj)[counter].author_name)
        info[counter]['fields']['tick_text'] = str(_('Это официальный аккаунт'))
        info[counter]['fields']['phone_num_name'] = str(_('Номер телефона'))
        counter+=1

    board_obj_json=json.dumps(info)

    return JsonResponse(data={
        'posts':board_obj_json,
        'total_result':totalData
    })