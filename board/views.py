from django.shortcuts import redirect, render
from .models import Board, City
from .forms import BoardForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services import add_advert, ajax_get_images, edit_adt, archive_adt, show_advertisement, show_index, load_more_index_adts

def index(request):
    return show_index(request)
@csrf_exempt
def load_more(request):
    return load_more_index_adts(request)

def advertisement(request,slug):
    return show_advertisement(request,slug)

@csrf_exempt 
def add_save(request):
    if request.method =='POST':
        form = BoardForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            add_advert(request, form)
            return HttpResponseRedirect('/')
        if request.is_ajax():
            return ajax_get_images(request)
        else:
            current_lang = get_language()
            if request.user.is_authenticated:
                context = {
                    'current_lang':current_lang,
                    'form':form,
                    'not_registered':False,
                }    
            else:
                context = {
                    'current_lang':current_lang,
                    'form':form,
                    'not_registered':True,
                }    
            return render(request, 'board/add.html', context)
    else:
        form = BoardForm()
        current_lang = get_language()
        if request.user.is_authenticated:
            context={
                'current_lang':current_lang,
                'form':form,
                'not_registered':False,
            }       
        else:
            context={
                'current_lang':current_lang,
                'form':form,
                'not_registered':True,
            }        
        return render(request, 'board/add.html', context) 
    

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

def load_branches(request):
    region_id = request.GET.get('region')
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'board/branch_dropdown_list_options.html', {'cities': cities})




def how_24h_works(request):
    current_lang = get_language() # для того, чтобы установить в шаблоне html ru или html uk 
    return render(request, 'others/24_hour.html', {'current_lang':current_lang})
def about_cookies(request):
    current_lang = get_language() # для того, чтобы установить в шаблоне html ru или html uk 
    return render(request, 'others/about_cookies.html', {'current_lang':current_lang})

def others_page(request):
    current_lang = get_language() # для того, чтобы установить в шаблоне html ru или html uk 
    return render(request, 'board/adaptive_others_page.html', {'current_lang':current_lang,})

def privacy_policy(request):
    current_lang = get_language()
    return render(request, 'others/privacy_policy.html', {'current_lang':current_lang})
def website_rules(request):
    current_lang = get_language()
    return render(request, 'others/website_rules.html', {'current_lang':current_lang})
def lawbook(request):
    current_lang = get_language()
    return render(request, 'others/lawbook.html', {'current_lang':current_lang})
def about_us(request):
    current_lang = get_language()
    return render(request, 'others/about_us.html', {'current_lang':current_lang})
def for_employers(request):
    return render(request, 'others/for_employers.html', {'current_lang':get_language()})

def error_to_admin(request):
    a=1/0
    return render(request, 'others/exception.html', {'current_lang':get_language()})

def handler400_error(request, *args, **argv):
    current_lang = get_language()
    return render(request, "others/400.html", {'current_lang': current_lang})
def handler403_error(request, *args, **argv):
    current_lang = get_language()
    return render(request, "others/403.html", {'current_lang': current_lang})
def handler404_error(request, *args, **argv):
    current_lang = get_language()
    return render(request, "others/404.html", {'current_lang': current_lang})
def handler500_error(request, *args, **argv):
    current_lang = get_language()
    return render(request, "others/500.html", {'current_lang': current_lang})