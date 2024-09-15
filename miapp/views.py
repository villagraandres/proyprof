from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
import logging
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import time


logger = logging.getLogger(__name__)
@csrf_exempt
def index(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            logger.warning(f"Login attempt with non-existent user: {email}")
            return render(request, 'login/index.html', {'error': 'User does not exist'})

        if user.check_password(password):
            if user.is_active:  # Use is_active instead of auth
                login(request, user)
                logger.info(f"User {email} logged in successfully.")
                return HttpResponseRedirect(reverse("dash"))
            else:
                logger.warning(f"Login attempt with inactive user: {email}")
                return render(request, 'login/index.html', {'error': 'Please confirm your account'})
        else:
            logger.warning(f"Wrong password attempt for user: {email}")
            return render(request, 'login/index.html', {'error': 'Wrong password'})

    return render(request, 'login/index.html')

def crear(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User(username=email, first_name=name, email=email)
            user.set_password(password)
            user.save()
            logger.info(f"User {email} created successfully.")
            return redirect('login')
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            return render(request, 'login/register.html', {'error': 'Email ya existe'})
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return render(request, 'login/register.html', {'error': 'Unexpected error occurred'})

    return render(request, 'login/register.html')



def dash(request):
    return render(request,"auth/dash.html")

def gen_frames():  
    cap = cv2.VideoCapture(0)  # Capture video from the first camera (0)
    
    while True:
        success, frame = cap.read()  # Read a frame
        if not success:
            frame = np.zeros((640, 480, 3), dtype=np.uint8)  # Black image
            cv2.putText(frame, 'No Feed', (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            logger.warning("No image feed, try restarting camera")
            
        else:
            # Encode frame as JPEG
            frame = cv2.resize(frame, (640, 480))
            
        time.sleep(0.034)
        # Yield frame in byte format
        yield (frame)
        
def format(frame):
    return()

# View for rendering the page with the video feed
def video_feed(request):
    
    frame = gen_frames()
    _, buffer = cv2.imencode('.jpg', frame)
        
    frame = buffer.tobytes()
    
    # Yield frame in byte format
    
    return StreamingHttpResponse(final, content_type='multipart/x-mixed-replace; boundary=frame')

def trans_feed(request):
    frame = gen_frames()
    frame2 = cv2.GaussianBlur(frame,(5,5),0)
    ret3,frame = cv2.threshold(frame2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    
    _, buffer = cv2.imencode('.jpg', frame)
        
    frame = buffer.tobytes()
    
    # Yield frame in byte format
    final = (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return StreamingHttpResponse(final, content_type='multipart/x-mixed-replace; boundary=frame')

# View to render the HTML template that will show the video feed
def camera(request):
    return render(request, 'camara/layout.html')