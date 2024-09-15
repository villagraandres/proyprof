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
framework = []
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

#def gen_trans():
   # cap = cv2.VideoCapture(0)  # Capture video from the first camera (0)
    
   # while True:
   #     success, frame = cap.read()  # Read a frame
   #     if not success:
   #         frame = np.zeros((640, 480, 3), dtype=np.uint8)  # Black image
   #         cv2.putText(frame, 'No Feed', (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
   #         logger.warning("No image feed, try restarting camera")
            
   #     else:
            # Encode frame as JPEG
   #         frame = cv2.resize(frame, (640, 480))
   #         frame = cv2.GaussianBlur(frame,(5,5),0)
   #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #         _,frame = cv2.threshold(frame,0,255,cv2.THRESH_BINARY)
            
        
  #      _, buffer = cv2.imencode('.jpg', frame)
        
 #       frame = buffer.tobytes()
        
        # Yield frame in byte format
#        yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames():  
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
                framework = cv2.warpPerspective(frame2, M, (480, 640))
            
            #cv2.drawContours(frame, approx, -1, (0,0,255), 3)
        
        _, buffer = cv2.imencode('.jpg', frame)
        
        frame = buffer.tobytes()
        
        # Yield frame in byte format
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
def screnie(request):
    frame = framework
    return HttpResponse(frame.tobytes(), content_type='image/jpeg')

# View for rendering the page with the video feed
def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

#def trans_feed(request):
#    return StreamingHttpResponse(gen_trans(), content_type='multipart/x-mixed-replace; boundary=frame')


# View to render the HTML template that will show the video feed
def camera(request):
    return render(request, 'camara/layout.html')