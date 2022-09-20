# Форма для создания объявлений на сайте
from django.forms import ModelForm, modelform_factory, DecimalField
from django import forms
from django.forms.widgets import Select
from .models import Board, Rubric, City, Image
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
    # Полное объявление
    # Валидация простая validators=[validators.RegexValidator(regex='^.{4,$')], error_messages={'invalid':'Слишком короткое название товара'}
    #price = forms.DecimalField(label='Цена', decimal_places=2) # decimal places - количество цифр в дробной части числа
    # rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
    #         label='Рубрика',help_text='Не забудьте выбрать рубрику',
    #         widget=forms.widgets.Select(attrs={'size':8}))
    #header_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    image1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=None)
    image2 = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=None)
    image3 = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=None)


    # Сложная валидация
    def clean(self):
        super().clean()
        errors = {}
        # if not self.cleaned_data['content']:
        #     errors['content']=ValidationError('Укажите имя')
        # if self.cleaned_data['price'] < 0:
        #     errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        # if errors:
        #     raise ValidationError(errors)

    class Meta:
        model = Board
        # Быстрое объявление
        #fields=('title','content', 'price', 'rubric', 'image1,', 'image2', 'image3')  
        fields=('image1', 'image2', 'image3', 'title','content', 'price', 'currency', 'workers_amount', 'rubric', 'age',  'region', 'city', 'author_name', 'phone_number', 'email')    
        labels={'title':'Название товара'}
        #  help_texts={'rubric':'Не забудьте выбрать рубрику'}
        # field_classes={'price':DecimalField}
        # widgets={'rubric':Select(attrs={'size':8})}  
        
        widgets = {
            'title':forms.TextInput(attrs={'class':'adt_name adt-name', 'placeholder':_('Введите, что будем делать')}),
            'price':forms.NumberInput(attrs={'min': '0', 'class': 'adt_name adt_salary', 'onblur':"getSal()", 'placeholder':'Оплата'}),
            'content':forms.Textarea(attrs={'class':'adt_desc', 'onkeyup':"charCount()", 'placeholder':_('Предлагаю написать адрес, место, условия работы и многое другое...')}),
            'author_name':forms.TextInput(attrs={'class':'contacts_author_name'}),
            'phone_number':forms.TextInput(attrs={'class':'contacts_phone_number'}),
            'email':forms.TextInput(attrs={'class':'contacts_email'}),
            'rubric':forms.Select(attrs={'class':'select_arrc'}),
            'age':forms.Select(attrs={'class':'select_arrc'}),
            'region':forms.Select(attrs={'class':'select_arrc'}),
            'city':forms.Select(attrs={'class':'select_arrc'}),
            'currency':forms.Select(attrs={'class':'select_currency'}),
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['rubric'].empty_label = None
        self.fields['rubric'].empty_label =_('--- Вид занятости ---') # '... Вид занятости ...'
        self.fields['age'].empty_label = _('Все')
        self.fields['region'].empty_label = '--- Область ---' # '... Область ...'
        self.fields['city'].empty_label = _('--- Город ---')# '... Город ...'
        self.fields['currency'].empty_label = None

        #self.fields['city'].queryset = City.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['city'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except ValueError:
                #pass  # invalid input from the client; ignore and fallback to empty City queryset
                self.fields['city'].queryset = City.objects.none()
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.region.city_set.order_by('name')  

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Image
        fields = ('image', )            