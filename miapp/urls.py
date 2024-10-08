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
    path('auth/crearExamen/<int:claseId>/',views.crearExamen,name="crearExamen"),
    path('auth/subir_excel',views.subir_excel,name="subir_excel"),
    path('camera/<int:claseId>/<int:examenId>',views.camera,name='camera'),
    path('live_feed',views.video_feed,name='live_feed'),
    path('screenshot',views.screnie,name='screenshot'),
    path('subir_imagen',views.subir_imagen,name='subir_imagen'),
     path('auth/listaex/<int:clase_id>/', views.listaex, name='listaex'),
     path('save',views.bruh,name='save'),
]