# cars/models.py
from django.db import models


class Car(models.Model):
    # Название автомобиля
    name = models.CharField(max_length=100)

    # Описание автомобиля
    description = models.TextField()

    # Цена за аренду
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    # Тип автомобиля (например, седан, внедорожник, спортивный и т.д.)
    car_type = models.CharField(max_length=50)

    # Статус автомобиля (доступен ли для аренды)
    available = models.BooleanField(default=True)

    # Изображение автомобиля
    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    # Дата добавления автомобиля
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
