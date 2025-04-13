# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from cars.models import Rental
from datetime import date
from decimal import Decimal


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход пользователя после регистрации
            messages.success(request, 'Аккаунт успешно создан! Вы можете войти в систему.')
            return redirect('cars:index')  # Убедитесь, что у вас есть URL с именем 'cars:index'
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



@login_required
def profile(request):
    rentals = Rental.objects.filter(user=request.user)
    today = date.today()  # ← это важная строка

    return render(request, 'users/profile.html', {
        'rentals': rentals,
        'today': today,  # ← обязательно передаём сюда
    })


@login_required
def replenish_balance(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount > 0:
                request.user.balance += amount
                request.user.save()
                messages.success(request, f"Баланс пополнен на {amount} ₽.")
            else:
                messages.error(request, "Введите положительное число.")
        except Exception as e:
            messages.error(request, "Некорректная сумма.")

    return redirect('users:profile')