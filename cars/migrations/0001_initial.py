# Generated by Django 5.2 on 2025-04-08 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_type', models.CharField(max_length=50)),
                ('available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
