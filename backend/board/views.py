from django.shortcuts import redirect, render
from .models import Board, TeenworkBlog
from .forms import BoardForm, TeenworkBlogForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services import *
from django.templatetags.static import static
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.admin.views import decorators
import functools
from googletrans import Translator
from utils.utils import ask_llm, translate_sentence
from django.forms.models import model_to_dict


def staff_member_required(view_func):  # переопределим декоратор
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('board:index')
    return functools.wraps(view_func)(_checklogin)

decorators.staff_member_required = staff_member_required 



def index(request):
    return show_index(request)
@csrf_exempt
def load_more(request):
    return load_more_index_adts(request)

def advertisement(request,slug):
    return show_advertisement(request,slug)


@csrf_exempt
def llm_chat(request):
    messages_list = json.loads(request.body.decode('utf-8'))

    messages_list_str = "\n\n".join([
        f"{msg['type']}:\n{msg['value']}"
        for msg in messages_list
    ])

    prompt = f'''
You are the manager of the Ukrainian platform for teenagers "Teenwork". 
Your task is to respond to users' requests within the scope of your duties as a manager.
Attached below is a chain of messages between the manager (assistant) and the user. 
Based on this chain, give a relevant answer.
Message chain:
-----------------------------
{messages_list_str}
-----------------------------
    '''.strip()
    prompt_en = translate_sentence(prompt)
    res = ask_llm(prompt_en, 'uk')
    res = res.replace('менеджер:', '').strip()

    return JsonResponse({
        'message': res
    })



@csrf_exempt
def llm_generate_job_desc(request):
    title = json.loads(request.body.decode('utf-8'))['title']
    prompt = f'''
    You are the manager of the Ukrainian platform for work for teenagers. 
    Your task is to generate a job description for the user based on the job title
    Generate a job description with 3000 chars.
    Title: {title}
    '''.strip()
    prompt_en = translate_sentence(prompt)
    res = ask_llm(prompt_en, 'uk')
    res = res.replace('менеджер:', '').strip()

    return JsonResponse({
        'description': res
    })


@csrf_exempt 
def add_save(request):
    if request.method =='POST':
        form = BoardForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            add_advert(request, form)
            if request.user.is_authenticated:
                return redirect('account:profile')
            return redirect('board:index')
        else:
            print(form.errors)
            if request.user.is_authenticated:
                context = {
                    'form':form,
                    'not_registered':False,
                }    
            else:
                context = {
                    'form':form,
                    'not_registered':True,
                }    
            return render(request, 'board/add.html', context)
    else:
        form = BoardForm()
        if request.user.is_authenticated:
            context={
                'form':form,
                'not_registered':False,
            }       
        else:
            context={
                'form':form,
                'not_registered':True,
            }        
        return render(request, 'board/add.html', context) 

def add_get_user_data(request):
    return get_user_data(request)
    

@login_required(login_url='/login/')
def edit(request, pk):
    return edit_adt(request, pk)
 
@login_required(login_url='/login/')
def delete(request,pk):
    if request.user == Board.objects.get(pk=pk).author:
        Board.objects.get(pk=pk).delete()
        return redirect('/profile/')
    else:
        return redirect('/profile/')

@login_required(login_url='/login/')
def archive(request, pk):
    return archive_adt(request, pk)

@login_required(login_url='/login/')
def get_ntu_students(request):
    # also we can search students, who are registered in out service
    # data = Account.objects.filter(im_working_student=True, email__contains="@nmu.one")
    
    data = [
        {
            'image': static('img/students/dmytro.jfif'),
            'name': 'Дмитро',
            'surname': 'Буслов',
            'patronymic': 'Юрійович',
            'speciality': '121-19-1',
            'faculty': 'ФІТ',
            'email': 'buslov.d.y@nmu.one',
            'city': 'Дніпро',
            'birthDate': '01.01.2001',
        },
        {
            'image': static('img/students/kristina.jfif'),
            'name': 'Кристина',
            'surname': 'Андрющенко',
            'patronymic': 'Сергіївна',
            'speciality': '121-19-1',
            'faculty': 'ФІТ',
            'email': 'andriushchenko.k.s@nmu.one',
            'city': 'Дніпро',
            'birthDate': '01.01.2001',
        },
        {
            'image': static('img/students/vladislav.jfif'),
            'name': 'Владислав',
            'surname': 'Федорець',
            'patronymic': 'Романович',
            'speciality': '121-19-1',
            'faculty': 'ФІТ',
            'email': 'fedorets.v.r@nmu.one',
            'city': 'Дніпро',
            'birthDate': '01.01.2001',
        },
        {
            'image': static('img/students/andriy.jfif'),
            'name': 'Андрій',
            'surname': 'Балян',
            'patronymic': 'Давідович',
            'speciality': '121-19-1',
            'faculty': 'ФІТ',
            'email': 'balian.a.d@nmu.one',
            'city': 'Дніпро',
            'birthDate': '01.01.2001',
        },
        {
            'image': static('img/students/karina.jfif'),
            'name': 'Карина',
            'surname': 'Жовнір',
            'patronymic': 'Олександрівна',
            'speciality': '121-19-1',
            'faculty': 'ФІТ',
            'email': 'zhovnir.k.o@nmu.one',
            'city': 'Дніпро',
            'birthDate': '01.01.2001',
        },
    ]
    university_info = {
        'image': 'https://lh3.googleusercontent.com/p/AF1QipM1veB6FAnZWcPP4jLBLpv1j1wkqJx4kiIpErtd=s1360-w1360-h1020',
        'title': 'Національний ТУ «Дніпровська політехніка»',
        'body': 'Національний технічний університет «Дніпровська політехніка» — провідний вищий навчальний заклад профілю України, заснований 16 червня 1899 р., розташований у місті Дніпро, Україна. Найстаріший вищий гірничий навчальний заклад в Україні, заснований як Катеринославський інститут.',
        'address': 'проспект Дмитра Яворницького, 19, Дніпро',
        'phone': '056 744 1411',
    }
    # return JsonResponse(data, status=200, safe=False)
    # return HttpResponse(data)
    return {'students': data, 'university': university_info}

@login_required(login_url='/login/')
def get_students(request, university):
    if university == 'ntu':
        data = get_ntu_students(request)
        return render(request, 'board/students.html', {'students':data['students'], 'university': data['university']})
    return render(request, 'board/students.html', {'students':[], 'university':[]})

def how_24h_works(request): 
    return render(request, 'others/24_hour.html')
def about_cookies(request): 
    return render(request, 'others/about_cookies.html')
def others_page(request): 
    return render(request, 'board/adaptive_others_page.html')
def privacy_policy(request):
    return render(request, 'others/privacy_policy.html')
def website_rules(request):
    return render(request, 'others/website_rules.html')
def lawbook(request):
    return render(request, 'others/lawbook.html')
def about_us(request):
    return render(request, 'others/about_us.html')
def for_employers(request):
    return render(request, 'others/for_employers.html')

def error_to_admin(request):
    a=1/0
    return render(request, 'others/exception.html')

def handler400_error(request, *args, **argv):
    return render(request, "others/400.html")
def handler403_error(request, *args, **argv):
    return render(request, "others/403.html")
def handler404_error(request, *args, **argv):
    return render(request, "others/404.html")
def handler500_error(request, *args, **argv):
    return render(request, "others/500.html")




            
def tw_blog(request):
    blog_obj = TeenworkBlog.objects.filter(status = 'published')
    paginator = Paginator(blog_obj, 20)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    
    time_now1 = str(datetime.today().date().day).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2)
    time_now2 = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

    context={
        'blog_obj':response, 
        'time_now1': time_now1,
        'time_now2': time_now2,
    }

    return render(request, 'others/blog.html', context)

from django.db.models import F
def tw_blog_post(request, slug):
    if TeenworkBlog.objects.filter(slug=slug).exists:
        blog_obj = TeenworkBlog.objects.get(slug=slug)
        TeenworkBlog.objects.filter(slug=slug).update(views=F('views')+1)
        return render(request, 'others/blog_post.html', {'blog_obj':blog_obj})
    else:
        return redirect('account:tw_blog')



'''
pip install googletrans==3.1.0a0
'''

def translate_str(string):
    string_trans = ''
    if get_language() == 'uk':
        try:
            # You can get about 1000 requests / hour without hitting the req/IP block limit. Also, individual requests are limited to less than 5000 characters per request
            translator = Translator()
            string_trans = translator.translate(string, dest='ru').text
        except Exception as e: print(e)

        return {'uk':string, 'ru':string_trans}
    elif get_language() == 'ru':
        try:
            # You can get about 1000 requests / hour without hitting the req/IP block limit. Also, individual requests are limited to less than 5000 characters per request
            translator = Translator()
            string_trans = translator.translate(string, dest='uk').text
        except Exception as e: print(e)

        return {'ru':string, 'uk':string_trans}

@staff_member_required
def add_blog_post(request):
    if request.method =='POST':
        form = TeenworkBlogForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.status = 'published'
            trans_title = translate_str(post.title)
            trans_content = translate_str(post.content)
            post.title_uk = trans_title['uk']
            post.title_ru = trans_title['ru']
            post.content_uk = trans_content['uk']
            post.content_ru = trans_content['ru']

            post.save()

            return redirect('board:tw_blog')
        else:
            return redirect('board:add_blog_post')
    else:
        form = TeenworkBlogForm()
        context={
            'form':form,
        }       
        return render(request, 'others/blog_post_add.html', context) 



@staff_member_required
def add_blog_post(request):
    if request.method =='POST':
        form = TeenworkBlogForm(data=request.POST)
        if form.is_valid():
            # ...
            return redirect('board:tw_blog')
        else:
            return redirect('board:add_blog_post')
    else:
        form = TeenworkBlogForm()
        # ...
        return render(request, 'others/blog_post_add.html', {}) 

