from django.shortcuts import render
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name='board'

urlpatterns = [
    path('add/', views.add_save , name='add'), 
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/archive/', views.archive, name='archive'),
    path('', views.index, name='index'),
    path('ad/<str:slug>/', views.advertisement, name='advertisement'),
    path('ajax/load-branches/', views.load_branches, name='ajax_load_branches'),
    path('load_more/',views.load_more,name='load_more'),

    path('how_24h_works/', views.how_24h_works, name='how_24h_works'),
    path('about_cookies/', views.about_cookies, name='about_cookies'),
    path('others_page/', views.others_page, name='others_page'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('rules/', views.website_rules, name='website_rules'),
    path('lawbook/', views.lawbook, name='lawbook'),
    path('about_us/', views.about_us, name='about_us'),
    path('for_employers/', views.for_employers, name='for_employers'),
    
    path('error_to_admin/', views.error_to_admin, name='error_to_admin'),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()