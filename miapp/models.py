from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import default_storage
# Create your models here.


class Clase(models.Model):
    nombre=models.CharField(max_length=60)
    
