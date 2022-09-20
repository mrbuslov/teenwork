from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from board.models import Age, City, Region, Rubric
from django.db.models import Q
from account.models import TeenworkBlog

# class StaticViewSitemap(Sitemap):
#     i18n = True # должны ли URL-адреса этой карты сайта создаваться с использованием всех ваших файлов LANGUAGES
#     # alternates = True # При использовании вместе с i18nсгенерированными URL-адресами каждый будет иметь список альтернативных ссылок, указывающих на другие языковые версии с использованием атрибута hreflang
#     # x_default = True # альтернативные ссылки, созданные с помощью, alternates будут содержать hreflang="x-default" резервную запись со значением LANGUAGE_CODE.
#     # changefreq = 'weekly'
#     # priority = 0.9

#     def items(self):
#         return['board:index']

#     def location(self, item):
#         return reverse(item)

        
    # def lastmod(self, obj):
    #     return obj.published


class RubricSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    protocol = 'https'
    
    def items(self):
        return Rubric.objects.all()

class AgeSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    protocol = 'https'
    protocol = 'https'
    
    def items(self):
        return Age.objects.all()


class RegionSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    protocol = 'https'
    
    def items(self):
        return Region.objects.all()


class CitySitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    protocol = 'https'
    
    def items(self):
        return City.objects.all()
        
        

class BlogSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    
    def items(self):
        return TeenworkBlog.objects.filter(status='published')