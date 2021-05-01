from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda req: redirect('/events'), name='redirect to index'),
    path('events', views.index, name='index'),
    path('routine', views.routine, name='routine'),
]
