from django.urls import path
from . import views
from .views import home, car_list, contact, login_view  # Добавляем login_view

app_name = 'cars'

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),

    path('cars/', car_list, name='list'),
]
