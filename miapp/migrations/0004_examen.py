# Generated by Django 5.1.1 on 2024-09-15 06:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0003_profile_clase_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pr', models.TextField()),
                ('maestro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examenes', to='miapp.profile')),
            ],
        ),
    ]
