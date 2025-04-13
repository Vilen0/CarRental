from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Car, CarType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from cars.models import Rental
from .models import Rental
from .forms import RentalForm
from django.contrib import messages

from datetime import timedelta, datetime


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
    cars = Car.objects.all()

    # Получение параметров фильтрации и сортировки из запроса
    car_type = request.GET.get('car_type')  # Получаем выбранный тип кузова (или None)
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    available = request.GET.get('available')
    sort = request.GET.get('sort')
    date_to = request.GET.get('date_to')

    # Применяем фильтры
    if car_type:
        # Фильтруем по ключу типа кузова, если выбран тип
        cars = cars.filter(car_types__key=car_type)

    if year_from:
        cars = cars.filter(year__gte=year_from)
    if year_to:
        cars = cars.filter(year__lte=year_to)

    if available == 'true':
        cars = cars.filter(available=True)
    elif available == 'false':
        cars = cars.filter(available=False)

    if date_to:
        try:
            date_to_dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            today = date.today()

            # Находим машины, у которых есть пересекающиеся аренды
            overlapping_rentals = Rental.objects.filter(
                start_date__lte=date_to_dt,
                end_date__gte=today
            ).values_list('car_id', flat=True)

            cars = cars.exclude(id__in=overlapping_rentals)

        except ValueError:
            pass  # Игнорируем ошибку даты, если пользователь ввёл что-то не то


    # Применяем сортировку
    if sort == 'price':
        cars = cars.order_by('price_per_day')
    elif sort == '-price':
        cars = cars.order_by('-price_per_day')
    elif sort == 'year':
        cars = cars.order_by('year')
    elif sort == '-year':
        cars = cars.order_by('-year')
    elif sort == 'car_type':
        cars = cars.order_by('car_types__name')

    # Получение уникальных значений для фильтров
    car_types = CarType.objects.all()
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'cars/index.html', {
        'cars': cars,
        'car_types': car_types,
        'years': years,
        'selected_car_type': car_type,  # Передаем выбранный тип кузова в шаблон
    })


@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user  # Присваиваем текущего пользователя
            rental.car = car  # Присваиваем выбранный автомобиль
            rental.save()
            return redirect('users:profile')  # Перенаправляем на профиль после успешного бронирования
    else:
        form = RentalForm()

    return render(request, 'cars/rent_car.html', {'car': car, 'form': form})



@login_required
def extend_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if request.method == 'POST':
        try:
            extra_days = int(request.POST.get('extra_days', 0))
            if extra_days > 0 and rental.end_date:
                rental.end_date += timedelta(days=extra_days)
                rental.save()
                messages.success(request, f"Аренда продлена на {extra_days} дней.")
            else:
                messages.error(request, "Некорректное количество дней.")
        except ValueError:
            messages.error(request, "Введите корректное число дней.")

    return redirect('users:profile')