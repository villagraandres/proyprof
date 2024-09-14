from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
# Create your views here.
def index(request):
    if request.method == 'POST':
         email=request.POST.get('email')
         password=request.POST.get('password')
    return render(request,'login/index.html')


def crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')  
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        try:
            user = User(username=email, first_name=nombre, email=email)
            user.set_password(password)
            user.save()
           
            return redirect('login')  
        except IntegrityError:
           
            return render(request, 'login/register.html', {'error': 'Email ya existe'})

    return render(request, 'login/register.html')
