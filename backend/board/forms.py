# Форма для создания объявлений на сайте
from django.forms import ModelForm, modelform_factory, DecimalField
from django import forms
from django.forms.widgets import Select
from .models import *
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import request
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator, MaxValueValidator
# Валидация занесённых данных с 271
# Изменение данных с 274
# Удаление с 275
class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields=('title','content', 'price', 'currency', 'workers_amount', 'rubric', 'age', 'city', 'author_name', 'phone_number', 'email')    
        labels={'title':'Название товара'}
        
        widgets = {
            'title':forms.TextInput(attrs={'class':'adt_name adt-name', 'placeholder':_('Введите, что будем делать')}),
            'price':forms.NumberInput(attrs={'min': '0', 'class': 'adt_name adt_salary', 'onblur':"getSal()", 'placeholder':'Оплата'}),
            'content':forms.Textarea(attrs={'class':'adt_desc', 'onkeyup':"charCount()", 'placeholder':_('Предлагаю написать адрес, место, условия работы и многое другое...')}),
            'author_name':forms.TextInput(attrs={'class':'contacts_author_name'}),
            'phone_number':forms.TextInput(attrs={'class':'contacts_phone_number'}),
            'email':forms.TextInput(attrs={'class':'contacts_email'}),
            'rubric':forms.Select(attrs={'class':'select_arrc'}),
            'age':forms.Select(attrs={'class':'select_arrc'}),
            'city':forms.TextInput(attrs={'class':'select_arrc', 'placeholder':_('Введите город')}),
            'currency':forms.Select(attrs={'class':'select_currency'}),
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['rubric'].empty_label = None
        self.fields['rubric'].empty_label =_('--- Вид занятости ---') # '... Вид занятости ...'
        self.fields['age'].empty_label = _('Все')
        self.fields['currency'].empty_label = None


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Image
        fields = ('image', )            



   
class TeenworkBlogForm(ModelForm):
    class Meta:
        model = TeenworkBlog
        fields=('title','content')

        widgets = {
            'title':forms.TextInput(attrs={'placeholder':_('Название публикации...')}), 
            'content':forms.Textarea(attrs={'placeholder':_('Описание публикации...')}), 
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

