from modeltranslation.translator import translator, TranslationOptions
from .models import Rubric, Region, City

class RubricTranslationOptions(TranslationOptions):
    fields = ('name',)

class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Rubric, RubricTranslationOptions)
translator.register(Region, RegionTranslationOptions)
translator.register(City, CityTranslationOptions)