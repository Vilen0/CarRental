from django.urls import path
from . import views
from .views import home, car_list, contact, login_view  # Добавляем login_view

app_name = 'cars'

urlpatterns = [
    path('', views.home, name='index'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('cars/', views.car_list, name='index'),
]
