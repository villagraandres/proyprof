from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for Profile can be added here

    def __str__(self):
        return self.user.username

class Clase(models.Model):
    nombre = models.CharField(max_length=60)
    profile = models.ForeignKey(Profile, related_name='clases', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Examen(models.Model):
    nombre = models.CharField(max_length=255)
    pags=models.IntegerField()
    num_preguntas = models.IntegerField()
    preguntas_y_respuestas = models.TextField()  
    maestro=models.ForeignKey(Profile,related_name='examenes',on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, related_name="clase", on_delete=models.CASCADE, null=True, blank=True)

class Estudiante(models.Model):
    nombre=models.CharField(max_length=100)
    matricula=models.IntegerField()
    calificaciones=models.TextField()
    clase=models.ForeignKey(Clase,related_name="clases",on_delete=models.CASCADE)


