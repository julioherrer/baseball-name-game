from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('start_game/', views.start_game, name='start_game'),
    path('start_recognition/', views.start_recognition, name='start_recognition'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('get_state/', views.get_state, name='get_state'),
    path('show_rules', views.show_rules, name='show_rules'),
    path('timer/', views.timer, name='timer'),
] 