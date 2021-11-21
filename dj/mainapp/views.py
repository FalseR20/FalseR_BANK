from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *


# получение данных из бд
def index(request):
    clients = Clients.objects.all()
    return render(request, "registration.html", {"clients": clients})


# сохранение данных в бд
def register(request):
    if request.method == "POST":
        client = Clients()
        client.login = request.POST.get("login")
        client.fullname = request.POST.get("fullname")
        client.password = request.POST.get("password")
        client.save()
    return HttpResponseRedirect("/")


# # получение данных из бд
# def index(request):
#     people = Person.objects.all()
#     return render(request, "registration.html", {"people": people})
#
#
# # сохранение данных в бд
# def create(request):
#     if request.method == "POST":
#         man = Person()
#         man.name = request.POST.get("name")
#         man.age = request.POST.get("age")
#         man.save()
#     return HttpResponseRedirect("/")
#
#
# # удаление всех данных из бд
# def delete(request):
#     if request.method == "POST":
#         people = Person.objects.all()
#         print("DELETING PERSON", people)
#         people.delete()
#     return HttpResponseRedirect("/")
