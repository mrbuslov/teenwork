# Форма для создания объявлений на сайте
from django.forms import ModelForm, modelform_factory, DecimalField
from django import forms
from django.forms.widgets import Select
from .models import Telegram
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import request
from board.models import City


class TelegramForm(ModelForm):
    class Meta:
        model = Telegram
        # Быстрое объявление
        fields=('telegram', 'rubric', 'age', 'region', 'city', 'person')   
        labels={'author':'Автор'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(TelegramForm, self).get_form(request, obj, **kwargs)
        if obj.some_model_field:
            obj.some_model_field = obj.related_model.prepopulating_model_field

        return form