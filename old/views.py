from django.shortcuts import render
from .models import LaundryMachine, Kasa, KasaPowerReading, DiscordHook
from django.http import JsonResponse
from django.core import serializers

# Create your views here.


def index(request):
    context1 = {
        "LaundryMachines": LaundryMachine.objects.all(),
        "Kasas": Kasa.objects.all(),
        "DiscordHooks": DiscordHook.objects.all(),
    }
    return render(request,"index.html",context=context1)

def data(request):
    context = {
        "LaundryMachines": LaundryMachine.objects.all(),
        "Kasas": Kasa.objects.all(),
    }
    return JsonResponse(model_to_dict(context))
