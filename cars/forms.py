# cars/forms.py
from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'description', 'price_per_day', 'car_type', 'available', 'image']
