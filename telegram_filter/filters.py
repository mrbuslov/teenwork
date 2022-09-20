from django_filters import rest_framework as filters 
from telegram_filter.models import Telegram
from django_filters import CharFilter
from board.models import Board, Rubric


class TelegramFilter(filters.FilterSet):
    #rubric = CharFilter(field_name = 'rubric', lookup_expr='in')
    #year = filters.RangeFilter()

    rubric = filters.ModelChoiceFilter(queryset=Telegram.objects.all())
    age  = filters.ModelChoiceFilter(queryset=Telegram.objects.all())
    region = filters.ModelChoiceFilter(queryset=Telegram.objects.all())
    city = filters.ModelChoiceFilter(queryset=Telegram.objects.all())

    class Meta:
        model = Telegram
        fields=['rubric', 'age', 'region', 'city']

