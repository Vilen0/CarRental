# cars/admin.py
from django.contrib import admin
from .models import Car, Rental
from .forms import CarForm


class CarAdmin(admin.ModelAdmin):
    form = CarForm


admin.site.register(Car, CarAdmin)
admin.site.register(Rental)

