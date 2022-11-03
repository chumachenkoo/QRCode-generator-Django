from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden
from django.template.response import TemplateResponse


def registration(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return HttpResponseRedirect('/login')


def account(request):
    return render(request, 'account.html')


def generator(request):
    return render(request, 'generator.html')