from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashbird-home'),
    path('about/', views.about, name='dashbird-about'),
]