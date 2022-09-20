import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import TextInput
from .models import Board
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _


class OrderFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="published", lookup_expr='gte')
    #end_date = DateFilter(field_name="published", lookup_expr='lte')
    title_content = CharFilter(field_name='title', method='title_content_filter', lookup_expr='icontains', widget=TextInput(attrs={'placeholder': _('Давайте поищем что-нибудь интересное...')}))
    price = django_filters.NumericRangeFilter(field_name='price', lookup_expr='range')
    class Meta:
        model = Board
        #exclude = ['header_image']
        fields = ['title_content','price','rubric', 'region', 'city', 'age']


    def title_content_filter(self, queryset, name, value):
        return Board.objects.filter(Q(title__icontains=value) | Q(content__icontains=value))




    # def translate(language, string):
    #     cur_lang = get_language()
    #     try:
    #         activate(language)
    #         print(language)
    #         print(string)
    #         text = _(string)
    #     finally:
    #         activate(cur_lang)
    #     return text

    