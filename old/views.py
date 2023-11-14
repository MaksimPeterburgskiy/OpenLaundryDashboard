from django.shortcuts import render
from .models import LaundryMachine, Kasa, KasaPowerReading, DiscordHook
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

# Create your views here.


def index(request):
    context1 = {
        "LaundryMachines": LaundryMachine.objects.all(),
        "Kasas": Kasa.objects.all(),
        "DiscordHooks": DiscordHook.objects.all(),
    }
    return render(request,"index.html",context=context1)

def machine_data(request):
    # return all machines serialized as json
    machines = LaundryMachine.objects.all()
    data = serializers.serialize("json", machines)
    return HttpResponse(data, content_type='application/json')
