from django.shortcuts import render


def index(request):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "mainapp/index.html", context=data)
