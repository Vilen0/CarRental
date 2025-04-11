from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Car

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

from django.shortcuts import render
from .models import Car

def car_list(request):
    cars = Car.objects.all()

    # Получение параметров фильтра и сортировки из запроса
    car_type = request.GET.get('car_type')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    available = request.GET.get('available')
    sort = request.GET.get('sort')

    # Применяем фильтры
    if car_type:
        cars = cars.filter(car_type=car_type)
    if year_from:
        cars = cars.filter(year__gte=year_from)
    if year_to:
        cars = cars.filter(year__lte=year_to)
    if available == 'true':
        cars = cars.filter(available=True)
    elif available == 'false':
        cars = cars.filter(available=False)

    # Применяем сортировку
    if sort == 'price':
        cars = cars.order_by('price_per_day')
    elif sort == 'year':
        cars = cars.order_by('year')
    elif sort == 'car_type':
        cars = cars.order_by('car_type')

    # Получение уникальных значений для фильтров
    car_types = Car.objects.values_list('car_type', flat=True).distinct()
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'cars/index.html', {
        'cars': cars,
        'car_types': car_types,
        'years': years,
    })
