# Generated by Django 4.2.13 on 2024-05-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
