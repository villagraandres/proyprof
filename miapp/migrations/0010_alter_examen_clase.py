# Generated by Django 5.1.1 on 2024-09-15 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0009_examen_clase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='clase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clase', to='miapp.clase'),
        ),
    ]
