# from typing_extensions import Required
from django.db import models
from django.core import validators
from slugify import slugify
from django.contrib.auth.models import User
from random import randint
from account.models import Account
from PIL import ExifTags, Image as PIL_Image
from datetime import date
import os
#from django.template.defaultfilters import slugify
from pytils.translit import slugify # djangoвская slugify не принимает кирилицу, поэтому пользоваться этой
from io import BytesIO
from django.core.files.base import ContentFile
import datetime
from django.urls import reverse
from django.contrib.sitemaps import ping_google
from django.utils.translation import get_language
import uuid
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Board(models.Model):
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    # image1 = models.ForeignKey('Image',null=True, blank=True, on_delete=models.CASCADE, related_name='image1')
    # image2 = models.ForeignKey('Image',null=True, blank=True, on_delete=models.CASCADE, related_name='image2')
    # image3 = models.ForeignKey('Image',null=True, blank=True, on_delete=models.CASCADE, related_name='image3')

    title = models.CharField(max_length=70, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка')
    content = models.TextField(max_length=5500, null=True, blank=True, verbose_name='Описание') 
    price = models.IntegerField(null=True, blank=True, verbose_name='Зарплата')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано') 

    rubric = models.ForeignKey('Rubric',null=True, on_delete=models.PROTECT,verbose_name='Рубрика')  
    region = models.ForeignKey('Region', on_delete=models.PROTECT, null=True, verbose_name='Область')
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, verbose_name='Город')
    age = models.ForeignKey('Age',null=True, blank=True, on_delete=models.PROTECT,verbose_name='Возраст') 
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True, verbose_name='Валюта')
    workers_amount = models.IntegerField(null=True, blank=True, verbose_name='Кол-во работников')


    author = models.ForeignKey('account.Account',null=True, on_delete=models.CASCADE, verbose_name='Автор', blank=True)
    author_name = models.CharField(max_length=50, verbose_name='Имя автора', blank=True)
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)

    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    #User
    favourites = models.ManyToManyField('account.Account', related_name="favourite", default=None, blank=True, verbose_name = "Понравившиеся публикации")
    workers = models.ManyToManyField('account.Account', related_name="workers", default=None, blank=True, verbose_name = "Принятые на работу")


    STATUS_CHOICES = (
        ('published', 'Published'),
        ('edited', 'Edited'),
        ('draft', 'Draft'),
        ('archive', 'Archive'),
        ('24hour', '24hour'),
        ('24hour_draft', '24hour_draft'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Изменение нашей модели для админ-панели
    class Meta:
        verbose_name_plural='Объявления' # verbose - подробный
        verbose_name= 'Объявление'
        ordering=['-published']
    
    # Чтобы в админ-панели отображалось фото
    def image_tag(self):
        photos = f''
        if self.image1:
            photos += f'<a href="/{self.image1}"><img src="/{self.image1}" width="150px" style="margin: 0 10px" /></a>'
        if self.image2:
            photos += f'<a href="/{self.image2}"><img src="/{self.image2}" width="150px" style="margin: 0 10px" /></a>'
        if self.image3:
            photos += f'<a href="/{self.image3}"><img src="/{self.image3}" width="150px" style="margin: 0 10px" /></a>'
       

        return mark_safe(photos)
    image_tag.short_description = 'Изображения'
    image_tag.allow_tags = True


    def save(self,  *args, **kwargs):
        if not self.pk:
            if Board.objects.filter(title=self.title).exists():
                # extra = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + str(uuid.uuid4())
            else:
                self.slug = slugify(self.title)
            super(Board, self).save(*args, **kwargs)
        else:
            super(Board, self).save(*args, **kwargs)

        try:
            ping_google() # Вы можете захотеть «пинговать» Google, когда ваша карта сайта изменится, чтобы он знал, что нужно переиндексировать ваш сайт
        except Exception:
            pass


    def delete(self, *args, **kwargs):
        deleted_adt = DeletedAds.objects.create(title = self.title, content = self.content, price = self.price, 
            published = self.published, rubric = self.rubric, region = self.region, city = self.city, age = self.age, 
            currency = self.currency, workers_amount = self.workers_amount, author = str(self.author), author_name = self.author_name, 
            phone_number = self.phone_number, email = self.email, views = self.views, status = self.status, 
        )
        for wrkr in self.workers.all():
            deleted_adt.workers.add(wrkr)
        deleted_adt.save()
        super(Board, self).delete(*args, **kwargs)

    def get_image_filename(instance, filename):
        title = instance.board.title
        slug = slugify(title)
        return "post_images/%s-%s" % (slug, filename) 






def get_img_dir():
    now = datetime.datetime.now()

    if os.path.isdir(f'images/{now.year}'):
        if os.path.isdir(f'images/{now.year}/{now.month}'):
            return str(f'images/{now.year}/{now.month}')
        else:
            os.mkdir(f'images/{now.year}/{now.month}')
            return get_img_dir()
    else:
        os.mkdir(f'images/{now.year}')
        return get_img_dir()

def translate(string):
    dic = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
        'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'E', 'ё':'e', 'Ж':'Zh', 'ж':'zh',
        'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'I', 'й':'i', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
        'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
        'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'Kh', 'х':'kh',
        'Ц':'Tc', 'ц':'tc', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Shch', 'щ':'shch', 'Ы':'Y',
        'ы':'y', 'Э':'E', 'э':'e', 'Ю':'Iu', 'ю':'iu', 'Я':'Ia', 'я':'ia'}
        
    alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
    

    st = string
    result = str()
    
    len_st = len(st)
    for i in range(0,len_st):
        if st[i] in alphabet:
            simb = dic[st[i]]
        else:
            simb = st[i]
        result = result + simb

    return result.replace(' ','_').lower()


from django.utils.safestring import mark_safe
class Image(models.Model):
    #board = models.ForeignKey(Board, default=None, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to=get_image_filename,
    #                           verbose_name='Image')
    image = models.ImageField() # upload_to="images/"
    adt = models.ForeignKey('Board',null=True, blank=True, on_delete=models.CASCADE,verbose_name='Публикация')  
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        # if not self.image:
        if self._state.adding: # У ModelStateобъекта есть два атрибута: addingфлаг , указывающий, Trueчто модель еще не была сохранена в базе данных, и db строка, относящаяся к псевдониму базы данных, из которого был загружен или сохранен экземпляр.
            image_dir = get_img_dir()

            filename = translate("%s.jpg" % self.image.name[:self.image.name.rfind('.')])
            image_format = self.image.name[self.image.name.rfind('.')+1:]
            
            image = PIL_Image.open(self.image) #.convert('RGB')
            # for PNG images discarding the alpha channel and fill it with some color
            # if image.mode in ('RGBA', 'LA'):
            #     background = PIL_Image.new(image.mode[:-1], image.size, '#fff')
            #     background.paste(image, image.split()[-1])
            #     image = background
            
            try:
                if image.mode != "RGB":
                    image = image.convert("RGB")
            except:
                pass

            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except:
                pass
            
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=70)

            # change the image field value to be the newly modified image value
            self.image.save(f'{image_dir}/{datetime.datetime.today().day}__{str(uuid.uuid4())}{filename}', ContentFile(image_io.getvalue()), save=False)

            super(Image, self).save(*args, **kwargs)
        else:
            super(Image, self).save(*args, **kwargs)
    
   




class Rubric(models.Model):
    name = models.CharField(max_length=50,db_index=True, verbose_name='Название')

    # Изменение нашей модели для админ-панели
    class Meta:
        verbose_name_plural='Рубрики' # verbose - подробный
        verbose_name= 'Рубрика'
        ordering=['name']
    
    # мы можем сделать подобным образом, так как у нас поле одно, а не несколько, как в Board(title,content...)
    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/uk/?rubriс={self.pk}'
        else:
            return f'/?rubriс={self.pk}'

class Age(models.Model):
    name = models.CharField(max_length=50,db_index=True, verbose_name='Возраст')

    class Meta:
        verbose_name_plural='Возраста' # verbose - подробный
        verbose_name= 'Возраст'
        ordering=['name']
    
    def __str__(self):
        return self.name

    
    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/uk/?age={self.pk}'
        else:
            return f'/?age={self.pk}'


class Region(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural='Области' # verbose - подробный
        verbose_name= 'Область'
    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/uk/?region={self.pk}'
        else:
            return f'/?region={self.pk}'

class City(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural='Города' # verbose - подробный
        verbose_name= 'Город'
    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/uk/?city={self.pk}'
        else:
            return f'/?city={self.pk}'

class Currency(models.Model):
    currency = models.CharField(max_length=10)
    
    class Meta:
        verbose_name_plural='Валюта' # verbose - подробный
        verbose_name= 'Валюта'
    def __str__(self):
        return self.currency







class DeletedAds(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название')
    content = models.TextField(max_length=5500, null=True, blank=True, verbose_name='Описание') 
    price = models.IntegerField(null=True, blank=True, verbose_name='Зарплата')
    published = models.DateTimeField(db_index=True, verbose_name='Опубликовано', editable=False) 

    rubric = models.ForeignKey('Rubric',null=True, on_delete=models.PROTECT,verbose_name='Рубрика')  
    region = models.ForeignKey('Region', on_delete=models.PROTECT, null=True, verbose_name='Область')
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True, verbose_name='Город')
    age = models.ForeignKey('Age',null=True, on_delete=models.PROTECT,verbose_name='Возраст') 
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True, verbose_name='Валюта')
    workers_amount = models.IntegerField(null=True, blank=True, verbose_name='Кол-во работников')

    author = models.CharField(max_length=50, null=True, verbose_name='Автор', blank=True)
    author_name = models.CharField(max_length=50, verbose_name='Имя автора', blank=True)
    phone_number = models.CharField(max_length=13, verbose_name='Номер телефона', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)

    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    workers = models.ManyToManyField('account.Account', related_name="deleted_adt_workers", default=None, blank=True, verbose_name = "Принятые на работу")

    status = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name_plural='Удалённые объявления' # verbose - подробный
        verbose_name= 'Удал. объявление'
    def __str__(self):
        return self.title

