from django.urls import path, re_path
from account import views as account_views
from telegram_filter import views
from django.contrib.auth import views as auth_views


app_name='account'

urlpatterns = [
    path('profile/', account_views.profile, name='profile'),
    path('profile_edit/', account_views.profile_edit, name='profile_edit'),
    path('by/<slug:username>/', account_views.account_profile, name='account_profile'),
    path('login/', account_views.user_login ,name='login'),
    path('account/user_logout/', account_views.user_logout, name='logout'),
    path('registration/', account_views.registration, name='registration'),
    path('resend_activation_email/', account_views.resend_activation_email, name='resend_activation_email'),
    path('activate/<uidb64>/<token>', account_views.VerificationView.as_view(), name = 'activate'),
    path('set_new_pswrd/<uidb64>/<token>', account_views.SetNewPswrdView.as_view(), name = 'set_new_pswrd'),
    path('reset_email/', account_views.RequestResetEmailView.as_view(), name = 'reset_email'),
    path('unsubscribe/<uidb64>/<token>', account_views.UnsubscribeView.as_view(), name = 'unsubscribe'),

    path('fav/<str:pk>/', account_views.favourite_add, name='favourite_add'),
    path('profile/favourites/', account_views.favourite_list, name='favourite_list'),

    path('blog/<str:slug>/', account_views.tw_blog_post, name='tw_blog_post'),
    path('blog/', account_views.tw_blog, name='tw_blog'),
]