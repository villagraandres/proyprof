from django.shortcuts import render, redirect,get_object_or_404
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
from .models import Clase, Profile,Examen # Import Profile
from google.cloud import vision
import io

logger = logging.getLogger(__name__)
@csrf_exempt
def index(request):
    #imagen()
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


def imagen():
    client = vision.ImageAnnotatorClient()

    with io.open(r'C:\Users\villa\Documents\proyprof\miapp\imagen.png', 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        print(f'Detected text: {text.description}')





def examenes(request, claseId):
    clase = get_object_or_404(Clase, id=claseId)
    return render(request, 'auth/examenes.html', {'clase': clase})


def clase(request,claseId):
    clase= get_object_or_404(Clase, id=claseId)
    return render(request,"auth/clase.html", {'clase': clase})

def crearExamen(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('examTitle')
        num_preguntas = int(request.POST.get('numQuestions'))
        pags = request.POST.get('pags')

        # Guardar el examen en la base de datos
        examen = Examen.objects.create(
            nombre=nombre,
            pags=pags,
            num_preguntas=num_preguntas,
            preguntas_y_respuestas=""  
        )
        
        respuestas_correctas = {}
        for i in range(1, num_preguntas + 1):
            respuesta = request.POST.get(f'correctAnswer{i}')
            if respuesta:
                respuestas_correctas[str(i)] = respuesta
        
        examen.preguntas_y_respuestas = json.dumps(respuestas_correctas)
        examen.save()

        return redirect('examenes')

    return render(request, 'auth/crearExamen.html')


def estudiantes(request,claseId):
    clase= get_object_or_404(Clase, id=claseId)
    return render(request,"auth/estudiantes.html")



def examenes(request):
    if request.method == 'POST':
        titulo_examen = request.POST.get('examTitle')
        num_preguntas = int(request.POST.get('numQuestions'))
        preguntas = []
        
        for i in range(1, num_preguntas + 1):
            pregunta = request.POST.get(f'question{i}')
            respuesta_correcta = request.POST.get(f'correctAnswer{i}')
            preguntas.append({
                'pregunta': pregunta,
                'respuesta_correcta': respuesta_correcta
            })
        
        # Aquí puedes hacer lo que necesites con los datos (guardar en base de datos, generar un archivo, etc.)
        
        return HttpResponse(f"Examen '{titulo_examen}' creado con {num_preguntas} preguntas.")
    
    return render(request, 'crear_examen.html')




