from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def home(request):
    return render(request, 'cars/index.html')

def contact(request):
    return render(request, 'cars/contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cars:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cars:index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def car_list(request):
    # Пока без базы данных — просто демонстрация
    cars = [
        {'name': 'Toyota Camry', 'price': '1000₽/день'},
        {'name': 'BMW X5', 'price': '2500₽/день'},
        {'name': 'Lada Vesta', 'price': '800₽/день'},
    ]
    return render(request, 'cars/car_list.html', {'cars': cars})
