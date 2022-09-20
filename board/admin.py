from django.contrib import admin
from django.http.request import QueryDict
from django.http.response import HttpResponseRedirect

from .models import Board, Rubric,Region,City, Image, Age, Currency, DeletedAds
from django.contrib.auth.models import Group
from django.shortcuts import redirect


def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
make_published.short_description = "Опубликовать объявления"
def make_24_published(modeladmin, request, queryset):
    queryset.update(status='24hour')
make_24_published.short_description = "Опубликовать объявления 24ч"



from datetime import datetime, timedelta
from django.db.models import Q
class adts_24_todelete(admin.SimpleListFilter):
    title = 'Дневные объявления(24ч)'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('more_24', 'Больше 24ч'), # если поменять название, то меняй второй параметр
            ('less_24', 'Меньше 24ч'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'more_24':
            # published = 
            return queryset.filter(Q(published__lte = (datetime.today() - timedelta(days=1))), Q(status='24hour'))
        if self.value() == 'less_24':
            return queryset.filter(Q(published__gte = (datetime.today() - timedelta(days=1))), Q(status='24hour'))    


class BoardAdmin(admin.ModelAdmin): # класс-редактор представления модели
    list_display=('title', 'published','rubric', 'status',)# последовательность имен полей, которые должны выводиться в списке записей
    list_display_links=('title',) # последовательность имен полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    search_fields = ('title','author__email') # последовательность имен полей, по которым должна выполняться фильтрация
    prepopulated_fields = {'slug': ('title',)} # slug применяет значение title
    ordering = ['status', 'published',]
    list_filter = ('status', adts_24_todelete) # поле с фильтрами справа
    fields = ( 'image_tag', 'image1','image2','image3','title','slug','content','price','rubric','region','city','age','currency','workers_amount','author','author_name','phone_number','email','views','favourites','workers','published','status')
    readonly_fields = ('image_tag', 'published')

    
    actions = [make_published, make_24_published]
    # change_list_template = "others/board_adt_save_btn.html"
    change_form_template = "others/board_adt_save_btn.html"


    
    # отвечает за кнопку ОПУБЛИКОВАТЬ и переход к след.публик.
    def response_change(self, request, obj):
        if "publish_btn" in request.POST:
            # не меняем status на published, потому что уже это сделали с js html admin
            self.message_user(request, f'Опубликована запись "{obj.title}"')
            
            if Board.objects.filter(pk = (obj.pk+1)).exists():
                return redirect(f"/teenwork_admin_page_secret/board/board/{Board.objects.get(pk = (obj.pk+1)).pk}/change")
            else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/board/board/')
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj_title = obj.title
            obj.delete()
            self.message_user(request, f'Удалена публикация "{obj_title}"')
            if Board.objects.filter(pk = next_obj).exists():
                return redirect(f"/teenwork_admin_page_secret/board/board/{Board.objects.get(pk = (next_obj)).pk}/change")
            else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/board/board/')
        elif "publish_24_btn" in request.POST:
            obj.status = '24hour'
            obj.save()
            self.message_user(request, f'Опубликована запись На 24 часа "{obj.title}"')
            
            if Board.objects.filter(pk = (obj.pk+1)).exists():
                return redirect(f"/teenwork_admin_page_secret/board/board/{Board.objects.get(pk = (obj.pk+1)).pk}/change")
            else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/board/board/')
        else:
                return HttpResponseRedirect('/teenwork_admin_page_secret/board/board/')
            

            



class DeletedAdsAdmin(admin.ModelAdmin): 
    list_display=('title', 'published','rubric',)
    list_display_links=('title',) 
    search_fields = ('title',) 
    list_filter = ('rubric',)  
    readonly_fields = ('published',)

class CityAdmin(admin.ModelAdmin): 
    list_display=('name', 'region',)
    list_display_links=('name',) 
    search_fields = ('name',) 




class ImagesFilter(admin.SimpleListFilter):
    title = 'Изображения'
    parameter_name = 'adt'

    def lookups(self, request, model_admin):
        return (
            ('empty', 'empty'), # если поменять название, то меняй второй параметр
            ('full', 'full'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'empty':
            return queryset.filter(adt = None)
        if self.value() == 'full':
            return queryset.exclude(adt = None)


class ImageAdmin(admin.ModelAdmin): 
    list_filter = (ImagesFilter,) 

    


admin.site.register(Board, BoardAdmin) # добавили на админ-панель
# admin.site.register(Rubric) # зарегестрировали Рубрику
# admin.site.register(Region)
# admin.site.register(City, CityAdmin)
admin.site.register(Image, ImageAdmin)
# admin.site.register(Age)
# admin.site.register(Currency)
admin.site.register(DeletedAds, DeletedAdsAdmin)

admin.site.unregister(Group)