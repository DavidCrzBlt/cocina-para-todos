# Generated by Django 4.2.13 on 2024-05-24 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_recipe_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='preparation_time',
            field=models.FloatField(),
        ),
    ]
