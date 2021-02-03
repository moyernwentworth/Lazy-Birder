from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def myfunctioncall(request):
    return HttpResponse("hello world")


def myfunctionabout(request):
    return HttpResponse("About Response")


def add(request, a, b):
    return HttpResponse(a+b)


def intro(request, name, age):
    my_dict = {
        "name": name,
        "age": age
    }
    return JsonResponse(my_dict)


def myfirstpage(request):
    return render(request, 'index.html')


def mysecondpage(request):
    return render(request, 'second.html')


def mythirdpage(request):
    var = 'hello wil'
    greeting = 'how are you'
    fruits = ['apple', 'mango', 'banana']
    num1, num2 = 3, 5
    ans = num1 < num2
    my_dict = {
        'var': var,
        'msg': greeting,
        'myfruits': fruits,
        'num1': num1,
        'num2': num2,
        'ans': ans
    }
    return render(request, 'third.html', context=my_dict)


def myimagepage(request):
    return render(request, 'imagepage.html')