from modeltranslation.translator import translator, TranslationOptions
from .models import TeenworkBlog

class TeenworkBlogTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

translator.register(TeenworkBlog, TeenworkBlogTranslationOptions)