# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Вы можете войти в систему.')
            return redirect('cars:index')  # Перенаправляем на главную страницу
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
