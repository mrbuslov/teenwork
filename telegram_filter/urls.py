from django.urls import path, include
from . import views

app_name='telegram_filter'

urlpatterns = [
    # path('telegram/', views.telegram, name='telegram'),
    path('telegram_bot/', views.get_unique_code, name='get_unique_code'),
]