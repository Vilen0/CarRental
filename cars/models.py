# cars/models.py
from django.db import models


class Car(models.Model):
    # Возможные типы автомобилей
    CAR_TYPE_CHOICES = [
        ('sedan', 'Седан'),
        ('suv', 'Внедорожник'),
        ('coupe', 'Купе'),
        ('hatchback', 'Хэтчбек'),
        ('convertible', 'Кабриолет'),
        ('van', 'Фургон'),
        ('pickup', 'Пикап'),
        ('sport', 'Спортивный'),
    ]

    # Название автомобиля
    name = models.CharField(max_length=100)

    # Описание автомобиля
    description = models.TextField()

    # Цена за аренду
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    # Выбор из списка
    car_type = models.CharField(
        max_length=20,
        choices=CAR_TYPE_CHOICES,
        default='sedan'
    )

    # Год выпуска
    year = models.PositiveIntegerField(default=2010)

    # Статус автомобиля (доступен ли для аренды)
    available = models.BooleanField(default=True)

    # Изображение автомобиля
    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    # Дата добавления автомобиля
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
