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