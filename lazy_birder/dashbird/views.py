from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'Wil Eddy',
        'title': 'Blog post',
        'content': 'First post',
        'date_posted': 'May 6, 2021'
    },
    {
        'author': 'Wil Eddy',
        'title': 'Blog post 2',
        'content': 'Second post',
        'date_posted': 'May 8, 2021'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'dashbird/home.html', context)


def about(request):
    return render(request, 'dashbird/about.html', {'title': 'About'})

