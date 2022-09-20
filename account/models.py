from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.core.cache import cache 
import datetime

from pytils.third.six import BytesIO
from website import settings
from PIL import ExifTags, Image as PIL_Image
from django.core.files.base import ContentFile
from django.utils.translation import get_language


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None, phone_number=None):
		if not email:
			raise ValueError('Введите email')
		if not username:
			raise ValueError('Введите никнейм')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			phone_number=phone_number,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


from django.contrib.auth.models import PermissionsMixin
class Account(AbstractBaseUser, PermissionsMixin):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	phone_number			= models.CharField(max_length=13, verbose_name='Номер телефона', blank=True, unique=True, null=True)
	date_joined				= models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='Последний вход', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_official 			= models.BooleanField(default=False)
	is_blocked				= models.BooleanField(default=False)
	first_name				= models.CharField(max_length=30, default='', blank=True)
	last_name				= models.CharField(max_length=30, default='', blank=True)
	unique_code				= models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	email_subscription		= models.BooleanField(default=True)
	
	is_asked_for_activ		= models.BooleanField(default=False)
	
	image 					= models.ImageField(null=True, blank=True)
	person_age 				= models.ForeignKey('board.Age',null=True, on_delete=models.PROTECT,verbose_name='Возраст', blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
# 	def has_perm(self, perm, obj=None):
# 		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
# 	def has_module_perms(self, app_label):
# 		return True

	# https://evileg.com/en/post/546/ - if user is online or not , но с записью в БД(((

	def save(self, *args, **kwargs):
		# if self._state.adding:
		if self.image:
			related_img = Account.objects.get(id=self.id)
			if related_img.image != self.image:
				filename = translate("%s.jpg" % self.image.name.split('.')[0])
			
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

				# change the image field value to be the newly modified image value
				self.image.save(f'images/users/{self.username}_{str(uuid.uuid4())}{filename}', ContentFile(image_io.getvalue()), save=False)
			
		super(Account, self).save(*args, **kwargs)



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
class SocialNets(models.Model):
	title = models.CharField(verbose_name='Название', max_length=200)
	img_src = models.ImageField(upload_to = 'images/social')
	email_content = models.TextField(verbose_name='Содержание email\'a')
	instagram_link = models.CharField(verbose_name='Ссылка на Инстаграм пост', max_length=200)
	facebook_link = models.CharField(verbose_name='Ссылка на Фейсбук пост', max_length=200)
	published = models.DateTimeField(auto_now_add=True,verbose_name='Опубликовано') 
	is_published = models.BooleanField(default=False, verbose_name='Публикация отправлена?')
	
	class Meta:
		verbose_name_plural='Публикации в соц.сетях'
		verbose_name= 'Публикация'	
		ordering=['-published']

	def image_tag(self):
		photos = f'<a href="{self.img_src.url}"><img src="{self.img_src.url}" width="150px" style="margin: 0 10px" /></a>'
		return mark_safe(photos)
	image_tag.short_description = 'Изображение'
	image_tag.allow_tags = True
			

	
	def __str__(self):
		return self.title


from slugify import slugify
from django.contrib.sitemaps import ping_google
class TeenworkBlog(models.Model):
	title_ru = models.CharField(verbose_name='Название', max_length=200)
	title_uk = models.CharField(verbose_name='Назва (uk)', max_length=200, blank=True, null=True)
	slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка', blank=True, null=True)
	img_src = models.CharField(verbose_name='Название фотографии', max_length=200, help_text='Пример: images/social/image.jpg')
	post_content_ru = models.TextField(verbose_name='Содержание post\'a')
	post_content_uk = models.TextField(verbose_name='Змiст post\'a (uk)', blank=True, null=True)
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

	def image_tag(self):
		photos = f'<a href="{self.img_src}"><img src="{self.img_src}" width="150px" style="margin: 0 10px" /></a>'
		return mark_safe(photos)
	image_tag.short_description = 'Изображение'
	image_tag.allow_tags = True
			

	
	def __str__(self):
		return self.title_ru


	def save(self,  *args, **kwargs):
		if not self.pk:
			if TeenworkBlog.objects.filter(title_ru=self.title_ru).exists():
				self.slug = slugify(self.title_ru) + "-" + str(uuid.uuid4())
			else:
				self.slug = slugify(self.title_ru)
			super(TeenworkBlog, self).save(*args, **kwargs)
		else:
			super(TeenworkBlog, self).save(*args, **kwargs)
			
		try:
			ping_google() # Вы можете захотеть «пинговать» Google, когда ваша карта сайта изменится, чтобы он знал, что нужно переиндексировать ваш сайт
		except Exception:
			pass
			
	def get_absolute_url(self): # sitemap
	    if get_language() == 'uk':
	        return f'/uk/blog/{self.slug}'
	    else:
	        return f'/blog/{self.slug}'
	        
	        
class Mailing(models.Model):
	title = models.CharField(verbose_name='Назва (uk)', max_length=200)
	img_src = models.CharField(verbose_name='Название фотографии', max_length=100, help_text='Пример: images/social/image.jpg')
	content = models.TextField(verbose_name='Змiст (uk)', blank=True, null=True)
	published = models.DateTimeField(auto_now_add=True,verbose_name='Отправлено') 
	views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

	
	class Meta:
		verbose_name_plural='Письма рассылки' # verbose - подробный
		verbose_name= 'Письмо'	
		ordering=['-published']

	def image_tag(self):
		photos = f'<a href="{self.img_src}"><img src="{self.img_src}" width="150px" style="margin: 0 10px" /></a>'
		return mark_safe(photos)
	image_tag.short_description = 'Изображение'
	image_tag.allow_tags = True
			
	def __str__(self):
		return self.title