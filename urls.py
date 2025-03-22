from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('start_game/', views.start_game, name='start_game'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('get_state/', views.get_state, name='get_state'),
    path('start_speech/', views.start_speech_recognition, name='start_speech'),
    path('save_score/', views.save_score, name='save_score'),
    path('show_rules/', views.show_rules, name='show_rules'),
    path('check_microphone/', views.check_microphone, name='check_microphone'),
] 