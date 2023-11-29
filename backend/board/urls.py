from django.shortcuts import render
from django.urls import include, path, re_path
from board import views, api
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='board'

urlpatterns_others = [
    path('how_24h_works/', views.how_24h_works, name='how_24h_works'),
    path('about_cookies/', views.about_cookies, name='about_cookies'),
    path('others_page/', views.others_page, name='others_page'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('rules/', views.website_rules, name='website_rules'),
    path('lawbook/', views.lawbook, name='lawbook'),
    path('about_us/', views.about_us, name='about_us'),
    path('for_employers/', views.for_employers, name='for_employers'),
    
    path('error_to_admin/', views.error_to_admin, name='error_to_admin'),

    path('blog/<str:slug>/', views.tw_blog_post, name='tw_blog_post'),
    path('blog/', views.tw_blog, name='tw_blog'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),
]

urlpatterns_api = [
    path('main_page_ads/', api.main_page_ads, name='main_page_ads')
]

urlpatterns = [
    path('add/', views.add_save , name='add'), 
    path('add/load_image/', views.add_load_image , name='add_load_image'), 
    path('add/get_user_data/', views.add_get_user_data , name='add_get_user_data'), 
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/archive/', views.archive, name='archive'),
    path('', views.index, name='index'),
    path('ad/<str:slug>/', views.advertisement, name='advertisement'),
    path('load_more/',views.load_more,name='load_more'),
    path('get_ntu_students/', views.get_ntu_students, name='get_ntu_students'),
    path('students/<str:university>/', views.get_students, name='get_students'),
    
    path('api/', include(urlpatterns_api)),

]
urlpatterns.extend(urlpatterns_others)
# urlpatterns.extend(urlpatterns_api)
