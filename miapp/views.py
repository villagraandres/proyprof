from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse  # Import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.conf import settings
import logging
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Clase, Profile,Examen,Estudiante # Import Profile
from google.cloud import vision
import io
import pandas as pd
import cv2
import numpy as np
import time
import cv2
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
import datetime
from os import path
import os
import re
from google.cloud import vision
from PIL import Image

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





def examenes(request,claseId):
    return render(request, 'auth/examenes.html',{'claseId':claseId})


def clase(request,claseId):
    clase= get_object_or_404(Clase, id=claseId)
    return render(request,"auth/clase.html", {'clase': clase})

def crearExamen(request,claseId):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('examTitle')
        num_preguntas = int(request.POST.get('numQuestions'))
        pags = request.POST.get('pags')
        perfil = get_object_or_404(Profile, user=request.user)

        clase = get_object_or_404(Clase, id=claseId)
        # Guardar el examen en la base de datos
        examen = Examen.objects.create(
            nombre=nombre,
            pags=pags,
            num_preguntas=num_preguntas,
            preguntas_y_respuestas="",
            maestro=perfil,
            clase=clase
        )
        

        respuestas_correctas = {}
        for i in range(1, num_preguntas + 1):
            respuesta = request.POST.get(f'correctAnswer{i}')
            if respuesta:
                respuestas_correctas[str(i)] = respuesta
        
        examen.preguntas_y_respuestas = json.dumps(respuestas_correctas)
        examen.save()

        

    return render(request, 'auth/crearExamen.html')



def subir_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        claseId=request.POST.get("claseId")
        df = pd.read_excel(excel_file)
        
        clase = get_object_or_404(Clase, id=claseId)

        for index, row in df.iterrows():
            Estudiante.objects.create(
                nombre=row['Nombre'],
                matricula=row['Matricula'],
                clase=clase
            )
        
        return redirect('some_view')  # Redirect to a view after processing
    return render(request, 'your_template.html')

def estudiantes(request,claseId):
    clase= get_object_or_404(Clase, id=claseId)
    estudiantes = Estudiante.objects.filter(clase=clase)
    return render(request,"auth/estudiantes.html",{"claseId":claseId,"estudiantes":estudiantes})




framework = []
def gen_frames():  
    global framework
    cap = cv2.VideoCapture(0)  # Capture video from the first camera (0)
    lastSux = []
    while True:
        success, frame = cap.read()  # Read a frame
        if not success:
            frame = np.zeros((640, 480, 3), dtype=np.uint8)  # Black image
            cv2.putText(frame, 'No Feed', (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            logger.warning("No image feed, try restarting camera")
            
        else:
            # Encode frame as JPEG
            frame = cv2.resize(frame, (640, 480))
            frame2 = cv2.GaussianBlur(frame,(5,5),0)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            #cv2.equalizeHist(frame2, frame2)
            frame2 = cv2.adaptiveThreshold(frame2,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
            #frame = cv2.Canny(frame2,60,180)
            
            shapes, hiera = cv2.findContours(frame2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #logger.info(shapes)
            maxAre = 0
            index = 0
            
            if not len(hiera):
                continue
            if len(hiera[0]):
                full = len(hiera[0])
                for x in range(full):
                    #pass
                    if hiera[0][x][0] == -1:
                        continue
                    #logger.warning(hiera[0][x])
                    area = cv2.contourArea(shapes[x])
                    if maxAre < area:
                        maxAre = area
                        index = x
                        
            epsilon = 0.05*cv2.arcLength(shapes[index],True)
            approx = cv2.approxPolyDP(shapes[index],epsilon,True)
            
            #cv2.drawContours(frame, shapes, index, (0,255,0), 3)
            
            if len(approx) == 4:
                lastSux = approx.copy()
            
            if len(lastSux):
                last = 3
                for x in range(4):
                    #cv2.circle(frame,approx[x][0], 10, (0,0,x*60), -1)
                    cv2.line(frame, lastSux[last][0], lastSux[x][0], (0, 0, 255), 3)
                    last = x
                
                pts1 = np.float32([[lastSux[0][0]], [lastSux[1][0]], [lastSux[2][0]], [lastSux[3][0]]])
                    
                pts2 = np.float32([[0, 0], [0, 640], [480, 640], [480, 0]])
                M = cv2.getPerspectiveTransform(pts1, pts2)
                framework = cv2.warpPerspective(frame, M, (480, 640))
            
            #cv2.drawContours(frame, approx, -1, (0,0,255), 3)
        
        _, buffer = cv2.imencode('.jpg', frame)
        
        frame = buffer.tobytes()
        #logger.warning("Frame ending")
        # Yield frame in byte format
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def screnie(request):
    global framework
    global selected
    selected = framework


    # Encode the frame as a JPEG image
    _, buffer = cv2.imencode('.jpg', selected)  

    # Convert the buffer to bytes
    frame_bytes = buffer.tobytes()
    
    # Return the image as an HTTP response
    return HttpResponse(frame_bytes, content_type='image/jpeg')

# View for rendering the page with the video feed
def video_feed(request):
       
    #    return render(request, 'camara/layout.html', context)
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

#def trans_feed(request):
#    return StreamingHttpResponse(gen_trans(), content_type='multipart/x-mixed-replace; boundary=frame')
@csrf_exempt  # Usar csrf_exempt solo en desarrollo si es necesario. Para producción, asegúrate de incluir correctamente el token CSRF.
def bruh(request):
    if request.method == 'POST':
       if request.method == 'POST' and request.FILES.get('image'):
        # Get the uploaded image
        image_file = request.FILES['image']
        claseId = request.POST.get('claseId')
        examenId = request.POST.get('examenId')

        # Read the image content and send it to Google's Vision API
        content = image_file.read()
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        # Extract the detected text
        detected_text = texts[0].description if texts else "No text detected."
        print(detected_text)
        # Try to extract the name and matricula using regex
        try:
            name_match = re.search(r"/Nombre:\s*([A-Za-z\s]+)", detected_text).group(1)
        except:
            name_match = "Random"
        try:
            matricula_match = re.search(r'Matricula: (\d+)', detected_text).group(1)
        except:
            matricula_match = 0

        print("Matricuka",matricula_match)
        responses = re.findall(r'Respuesta: ([A-Z])', detected_text)

        # Fetch exam and class from the database
        examen = get_object_or_404(Examen, id=examenId)
        clase = get_object_or_404(Clase, id=claseId)

        print("La clase es ",claseId)
        # Compare responses and calculate the score
        respuestas = re.findall(r'([A-Z])', examen.preguntas_y_respuestas)
        preguntas = len(respuestas)
        calificacion = sum(100 / preguntas for alumno, maestro in zip(responses, respuestas) if alumno == maestro)

        try:
            # Find student by matricula and update their scores
            matched_estudiante = Estudiante.objects.get(matricula=matricula_match, clase=clase)
            existing_calificaciones = matched_estudiante.calificaciones or ''
            updated_calificaciones = f"{existing_calificaciones}, {calificacion}" if existing_calificaciones else str(calificacion)
            matched_estudiante.calificaciones = updated_calificaciones
            matched_estudiante.save()

        except Estudiante.DoesNotExist:
            matched_estudiante = None
            print('No matching Estudiante found')

        # Return the detected text for debugging
        url = reverse('examenes', kwargs={'claseId': claseId})

        # Redirect to the constructed URL
        return redirect(url)


# View to render the HTML template that will show the video feed
def camera(request,claseId,examenId):

    context = {
            "active": False,
            'claseId':claseId,
            'examenId':examenId
        }
    #if request.method == "POST":
    #    request.POST.get("btnTomarFoto")
    #    context["active"] = True
    #    return render(request, 'camara/layout.html', context)

    return render(request, 'camara/layout.html', context)

def subir_imagen(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        claseId=request.POST.get('claseId')
        examenId=request.POST.get('examenId')
        print(claseId)
        print("adsdasd")
         
        content = image_file.read()
        vision_client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            detected_text = texts[0].description
            print(detected_text)
        else:
            detected_text = "No text detected."
        # Extract information using regex
        try:
            name_match = re.search(r"Nombre:\s*([A-Za-z\s]+)", detected_text).group(1)
        except:
            name_match = "Random"

        try:    
             matricula_match = re.search(r'Matricula:\s*(\d+)', detected_text).group(1)
        except:
            matricula_match = 0
        print("LA MATRICUKA",matricula_match)
        
        responses = re.findall(r'Respuesta: ([A-Z])', detected_text)
        

        examen = get_object_or_404(Examen, id=examenId)
        clase = get_object_or_404(Clase, id=claseId)

        respuestas = re.findall(r'([A-Z])', examen.preguntas_y_respuestas)
        preguntas = len(respuestas)
        calificacion = 0
        
        for alumno,maestro in zip(responses,respuestas):
            print(alumno,maestro)
            if alumno == maestro:
                calificacion+=100/preguntas

        print("La calificacion es",calificacion)
        try:
            matched_estudiante = Estudiante.objects.get(matricula=matricula_match, clase=clase)
            print(f'Matched Estudiante: {matched_estudiante.nombre}')
            existing_calificaciones = matched_estudiante.calificaciones
            if existing_calificaciones:
                updated_calificaciones = f"{existing_calificaciones}, {calificacion}"
            else:
                updated_calificaciones = str(calificacion)
            matched_estudiante.calificaciones = updated_calificaciones
            matched_estudiante.save()
            print(f'Updated Calificaciones: {matched_estudiante.calificaciones}')
        except Estudiante.DoesNotExist:
            matched_estudiante = None
            print('No matching Estudiante found')
    
        url = reverse('estudiantes', kwargs={'claseId': claseId})

        # Redirect to the constructed URL
        return redirect(url)
        

      

    return render(request, 'upload_image.html')


def listaex(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    examenes = Examen.objects.filter(clase=clase)
    return render(request, 'auth/lista_examenes.html', {'clase': clase, 'examenes': examenes})