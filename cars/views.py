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
from django.db.models import Q, Count
from django.utils import timezone

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
        cars = cars.filter(car_types__key=car_type)

    if year_from:
        cars = cars.filter(year__gte=year_from)
    if year_to:
        cars = cars.filter(year__lte=year_to)

    today = timezone.now().date()

    # Если параметр 'available' отсутствует в запросе, то принимаем его как 'all'
    if available is None:
        available = ''

    # Фильтрация по доступности
    if available == 'true':
        cars = cars.exclude(Q(rental__end_date__gte=today) & Q(rental__end_date__isnull=False)).distinct()
    elif available == 'false':
        cars = cars.filter(Q(rental__end_date__gte=today) & Q(rental__end_date__isnull=False)).distinct()
    elif available == 'all':
        pass  # Отображаем все автомобили без фильтрации

    # Собираем информацию о доступности каждого автомобиля
    for car in cars:
        active_rentals = car.rental_set.filter(end_date__gte=today)
        if active_rentals.exists():
            car.status = 'Недоступен'
            car.unavailable_until = active_rentals.first().end_date
        else:
            car.status = 'Доступен'

    # Обработка аренды по дате
    if date_to:
        try:
            date_to_dt = datetime.strptime(date_to, '%Y-%m-%d').date()

            # Исключаем автомобили с пересекающимися арендами
            overlapping_rentals = Rental.objects.filter(
                start_date__lte=date_to_dt,
                end_date__gte=today
            ).values_list('car_id', flat=True)

            cars = cars.exclude(id__in=overlapping_rentals)

        except ValueError:
            pass  # Игнорируем ошибку, если дата неверна

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
        'available': available,  # Передаем параметр доступности в шаблон
        'today': today,  # Передаем текущую дату в шаблон
  # Передаем информацию о доступности
    })


@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Проверяем, доступен ли автомобиль
    if car.status != 'Доступен' and car.unavailable_until:
        # Если автомобиль недоступен, проверяем, если дата окончания доступности меньше сегодняшней даты
        if car.unavailable_until >= date.today():
            # Если автомобиль все еще недоступен, выводим сообщение
            message = f"Этот автомобиль недоступен до {car.unavailable_until}."
            return render(request, 'cars/rent_car.html', {'car': car, 'message': message})

    # Если автомобиль доступен, или дата окончания доступности прошла
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = request.user

            # Обновляем статус автомобиля и устанавливаем дату, до которой он недоступен
            car.status = 'Недоступен'
            car.unavailable_until = rental.end_date  # Пример: аренда заканчивается в поле end_date формы
            car.save()  # Сохраняем изменения в автомобиле

            rental.save()  # Сохраняем аренду в базе данных
            return redirect('users:profile')  # Перенаправление после успешной аренды
    else:
        form = RentalForm()

    return render(request, 'cars/rent_car.html', {'car': car, 'form': form})


@login_required
def extend_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)
    car = rental.car

    if request.method == 'POST':
        try:
            extra_days = int(request.POST.get('extra_days', 0))
            if extra_days > 0 and rental.end_date:
                rental.end_date += timedelta(days=extra_days)
                rental.save()

                car.unavailable_until = rental.end_date
                car.status = 'Недоступен'  # Обновляем статус на "Недоступен"
                car.save()


                messages.success(request, f"Аренда продлена на {extra_days} дней.")
            else:
                messages.error(request, "Некорректное количество дней.")
        except ValueError:
            messages.error(request, "Введите корректное число дней.")

    return redirect('users:profile')