from django.contrib import admin
from django.urls import path, include, re_path
from account.views import user_logout
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from website import settings
from .sitemaps import RubricSitemap, AgeSitemap, RegionSitemap, CitySitemap,BlogSitemap # Sitemap
from django.contrib.sitemaps.views import sitemap, index
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name='website'

urlpatterns = [
    path('teenwork_admin_page_secret/', admin.site.urls),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()

sitemaps = {
    'rubric': RubricSitemap,
    'age': AgeSitemap,
    'region': RegionSitemap,
    'city': CitySitemap,
    'blog':BlogSitemap,
}


urlpatterns += i18n_patterns (
    # path('admin/', admin.site.urls),
    
    path('chat/', include('chat.urls')),
    path('',include('account.urls', namespace='account')),
    path('', include('telegram_filter.urls', namespace='telegram_filter')),

    path('', include('board.urls', namespace='board')),

    # path('sitemap.xml', sitemap, {'sitemaps':sitemaps}),
    
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    prefix_default_language=False # чтобы не было /ru/ в строке
)

# if 'rosetta' in settings.INSTALLED_APPS: # это графический редактор переведённого текста
#     urlpatterns += [
#         re_path(r'^teenwork_page_rosetta_secret/', include('rosetta.urls'))
#     ]

admin.site.index_title = "TeenWork"
admin.site.site_header = "TeenWork Admin"
admin.site.site_title = "Admin"


# errors handlers
# handler400 = 'board.views.handler400_error' # неверный запрос
handler403 = 'board.views.handler403_error' # запрещён доступ к странице
handler404 = 'board.views.handler404_error' # неверная страница
handler500 = 'board.views.handler500_error' # проблема с сервером