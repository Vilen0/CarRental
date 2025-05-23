
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('Доступен', 'Доступен'),
    ('Недоступен', 'Недоступен'),
]

class CarType(models.Model):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_types = models.ManyToManyField(CarType)
    year = models.PositiveIntegerField(default=2010)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Доступен')
    unavailable_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name




class Rental(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name} ({self.start_date} → {self.end_date})"
