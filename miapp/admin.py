from django.contrib import admin
from django.contrib.auth.models import User
from .models import Clase, Profile,Examen


admin.site.register(Clase)
admin.site.register(Profile)
admin.site.register(Examen)