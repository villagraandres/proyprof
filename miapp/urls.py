from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('crear',views.crear,name='crear'),
    path('auth/dash',views.dash,name='dash'),
    path('auth/clase',views.clase,name='clase'),
    path('auth/crearClase',views.crearClase,name="crearClase")
]