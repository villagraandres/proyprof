from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.
def index(request):
    if request.method == 'POST':
         email=request.POST.get('email')
         password=request.POST.get('password')
    return render(request,'layout.html')

def crear(request):
    if request.method=='POST':
        nombre=request.POST['nombre']
        email=request.POST['email']
        password=request.POST['password']


