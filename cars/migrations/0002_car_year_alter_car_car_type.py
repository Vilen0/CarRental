# Generated by Django 5.2 on 2025-04-11 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(default=2010),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_type',
            field=models.CharField(choices=[('sedan', 'Седан'), ('suv', 'Внедорожник'), ('coupe', 'Купе'), ('hatchback', 'Хэтчбек'), ('convertible', 'Кабриолет'), ('van', 'Фургон'), ('pickup', 'Пикап'), ('sport', 'Спортивный')], default='sedan', max_length=20),
        ),
    ]
