from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('crear',views.crear,name='crear'),
    path('auth/dash',views.dash,name='dash'),
    path('auth/clase/<int:claseId>/',views.clase,name='clase'),
    path('auth/crearClase',views.crearClase,name="crearClase"),
    path('auth/estudiantes/<int:claseId>/',views.estudiantes,name="estudiantes"),
    path('auth/examenes/<int:claseId>/',views.examenes,name="examenes"),
    path('auth/crearExamen',views.crearExamen,name="crearExamen"),
]