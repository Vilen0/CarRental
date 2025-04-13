# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('replenish/', views.replenish_balance, name='replenish_balance'),  # вот он
    path('manage/<int:user_id>/', views.manage_user, name='manage_user'),

]
