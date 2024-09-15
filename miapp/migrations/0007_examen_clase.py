# Generated by Django 5.1.1 on 2024-09-15 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0006_examen_pags'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='clase',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='clase', to='miapp.clase'),
            preserve_default=False,
        ),
    ]
