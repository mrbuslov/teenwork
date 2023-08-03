from django.db import models
from random import randint
from PIL import ExifTags, Image as PIL_Image
import os
from pytils.translit import slugify # djangoвская slugify не принимает кирилицу, поэтому пользоваться этой
from io import BytesIO
from django.core.files.base import ContentFile
import datetime
from django.contrib.sitemaps import ping_google
from django.utils.translation import get_language
import uuid
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe

class Board(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка')
    content = models.TextField(max_length=5500, null=True, blank=True, verbose_name='Описание') 
    price = models.IntegerField(null=True, blank=True, verbose_name='Зарплата')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано') 

    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT,verbose_name='Рубрика')  
    city = models.CharField(max_length=100,  verbose_name='Город')
    age = models.ForeignKey('Age',null=True, blank=True, on_delete=models.PROTECT,verbose_name='Возраст', related_name='age') 
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
        verbose_name_plural=_('Объявления') # verbose - подробный
        verbose_name= _('Объявление')
        ordering=['-published']
    
    # Чтобы в админ-панели отображалось фото
    def image_tag(self):
        images = Image.objects.filter(board=self)
        photos = f''
        for i in images:
            photos += f'<a href="/{i.url}"><img src="/{i}" width="150px" style="margin: 0 10px" /></a>'
        return mark_safe(photos)

    image_tag.short_description = _('Изображения')
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
            published = self.published, rubric = self.rubric, city = self.city, age = self.age,
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


    def get_image(self):
        return Image.objects.filter(board=self, position=0).first().image.url
    
    def get_images(self):
        return Image.objects.filter(board=self)



class Image(models.Model):
    image = models.ImageField(max_length=300)
    board = models.ForeignKey(Board, null=True, blank=True, on_delete=models.CASCADE,verbose_name='Объявление')  
    position = models.PositiveSmallIntegerField(default=1, verbose_name=_("Позиция"))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self._state.adding: 
            image_dir = self.get_img_dir()
            filename = str(uuid.uuid4()) + '.jpg'

            image = PIL_Image.open(self.image)
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
            self.image.save(f'{image_dir}/{filename}', ContentFile(image_io.getvalue()), save=False)
            
        super(Image, self).save(*args, **kwargs)
            

    def get_img_dir(self):
        now = datetime.datetime.now()

        if os.path.isdir(f'images/{now.year}'):
            if os.path.isdir(f'images/{now.year}/{now.month}'):
                return str(f'{now.year}/{now.month}') # return without images because MEDIA_PATH will take care of it while saving
            else:
                os.mkdir(f'images/{now.year}/{now.month}')
                return self.get_img_dir()
        else:
            os.mkdir(f'images/{now.year}')
            return self.get_img_dir()

    
    class Meta:
        verbose_name_plural=_('Фотографии')
        verbose_name= _('Фотография')
        ordering=['id']

class Rubric(models.Model):
    name = models.CharField(max_length=50,db_index=True, verbose_name='Название')

    class Meta:
        verbose_name_plural='Рубрики' 
        verbose_name= 'Рубрика'
        ordering=['name']
    
    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'en':
            return f'/en/?rubriс={self.pk}'
        else:
            return f'/?rubriс={self.pk}'



class Age(models.Model):
    # from board.models import Age
    # for i in range(17,41):
    #     Age.objects.create()
    name = models.PositiveIntegerField(db_index=True, verbose_name='Возраст')

    class Meta:
        verbose_name_plural='Возраста' # verbose - подробный
        verbose_name= 'Возраст'
        ordering=['name']
    
    def __str__(self):
        return f'{self.name}'

    
    def get_absolute_url(self): # sitemap
        if get_language() == 'en':
            return f'/en/?age={self.pk}'
        else:
            return f'/?age={self.pk}'

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
    city = models.CharField( max_length=100, null=True, verbose_name='Город')
    age = models.ForeignKey('Age',null=True, on_delete=models.PROTECT,verbose_name='Возраст от', related_name='age_deleted') 
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

class TeenworkBlog(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка', blank=True, null=True)
    content = RichTextUploadingField(verbose_name='Содержание post\'a', blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True,verbose_name='Опубликовано') 
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')    
    
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
	
    class Meta:
        verbose_name_plural='Публикации блога' # verbose - подробный
        verbose_name= 'Публикация'	
        ordering=['-published']



    def __str__(self):
        return self.title


    def save(self,  *args, **kwargs):
        if not self.pk:
            if TeenworkBlog.objects.filter(title=self.title).exists():
                self.slug = slugify(self.title) + "-" + str(uuid.uuid4())
            else:
                self.slug = slugify(self.title)
            super(TeenworkBlog, self).save(*args, **kwargs)
        else:
            super(TeenworkBlog, self).save(*args, **kwargs)
            
        try: 
            ping_google(sitemap_url='/sitemap.xml', sitemap_uses_https=True) # Вы можете захотеть «пинговать» Google, когда ваша карта сайта изменится, чтобы он знал, что нужно переиндексировать ваш сайт
        except Exception: 
            print('cannot ping Google')
            raise Exception('cannot ping Google')

    def get_absolute_url(self): # sitemap
        if get_language() == 'en':
            return f'/blog/{self.slug}/'
        else:
            return f'/en/blog/{self.slug}/'