import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import TextInput
from .models import Board, Age
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class OrderFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="published", lookup_expr='gte')
    #end_date = DateFilter(field_name="published", lookup_expr='lte')
    title_content = CharFilter(field_name='title', method='title_content_filter', lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Давайте поищем что-нибудь интересное...')}))
    age = django_filters.ModelChoiceFilter(field_name='age', method='age_all_filter', queryset=Age.objects.all())
    price = django_filters.NumericRangeFilter(field_name='price', lookup_expr='range')
    class Meta:
        model = Board
        fields = ['title_content','price','rubric', 'city', 'age']


    def title_content_filter(self, queryset, name, value):
        return Board.objects.filter(Q(title__icontains=value) | Q(content__icontains=value))
        
    def age_all_filter(self, queryset, name, value):
        print(value)
        if value != None:
            return Board.objects.filter(Q(age=value) | Q(age=None))
        return Board.objects.all()
        # return Age.objects.all()
