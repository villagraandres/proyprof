from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('crear',views.crear,name='crear'),
    path('auth/dash',views.dash,name='dash'),
    path('camera',views.camera,name='camera'),
    path('live_feed',views.video_feed,name='live_feed'),
    path('screenshot',views.screnie,name='screenshot'),
    #path('trans_feed',views.trans_feed,name='trans_feed'),
]