from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse  # Import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
import logging
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Clase, Profile  # Import Profile

logger = logging.getLogger(__name__)
@csrf_exempt
def index(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
           
            return render(request, 'login/index.html', {'error': 'El usuario no existe'})

        if user.check_password(password):
            if user.is_active:  
                login(request, user)
                logger.info(f"User {email} logged in successfully.")
                return HttpResponseRedirect(reverse("dash"))
            
        else:
          
            return render(request, 'login/index.html', {'error': 'Contrasena incorrecta'})

    return render(request, 'login/index.html')


def crear(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

       
        if not name or not email or not password:
            logger.warning("Attempt to create user with empty fields.")
            return render(request, 'login/register.html', {'error': 'Todos los campos son requeridos'})

        try:
            user = User(username=email, first_name=name, email=email)
            user.set_password(password)
            user.save()

            Profile.objects.create(user=user)
            logger.info(f"User {email} created successfully.")
            return redirect('login')
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            return render(request, 'login/register.html', {'error': 'Email already exists.'})
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return render(request, 'login/register.html', {'error': 'Unexpected error occurred.'})

    return render(request, 'login/register.html')

@csrf_exempt
def crearClase(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get('name')
            user_id = data.get('user_id')
            print(nombre)
            print(user_id)
            print("daksjdaskjdalskdjalskdjaslkdj______")
            
            user = User.objects.get(id=user_id)
            print("---")
            print(user)
             
            profile = Profile.objects.get(user=user)
            
            print("---")
            print(profile)
            clase = Clase(nombre=nombre, profile=profile)
            clase.save()

            
            return JsonResponse({'message': 'Class created successfully', 'class_id': clase.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no existe'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def dash(request):
    user_id = request.user.id
    try:
        profile = Profile.objects.get(user_id=user_id)
        clases = profile.clases.all()  

        print(clases)
        return render(request, "auth/dash.html", {'user_id': user_id, 'clases': clases})
    except Profile.DoesNotExist:
        return render(request, "auth/dash.html", {'user_id': user_id, 'clases': []})

def clase(request):
    return render(request,"auth/clase.html")

def estudiantes(request):
    return render(request,"auth/estudiantes.html")