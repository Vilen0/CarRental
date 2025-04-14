# cars/forms.py
from django import forms
from .models import Car, Rental

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'description', 'price_per_day', 'car_types', 'available', 'image']


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name and not cleaned_data.get("description"):
            # Поиск первого авто с таким же именем и заполненным описанием
            similar_car = Car.objects.filter(name=name).exclude(description="").first()
            if similar_car:
                cleaned_data["description"] = similar_car.description

        return cleaned_data


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental

        fields = ['end_date']
        labels = {
            'end_date': 'Дата окончания аренды',
        }
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
