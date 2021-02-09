from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('<h1>Dashbird Home<h1>')


def about(request):
    return HttpResponse('<h1>Dashbird About<h1>')
