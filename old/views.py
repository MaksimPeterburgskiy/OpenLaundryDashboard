from django.shortcuts import redirect, render
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

def set_available(request, pk):
    # get machine by pk
    machine = LaundryMachine.objects.get(pk=pk)
    # set machine to available
    machine.status = "A"
    # save machine
    machine.save()
    # return success
    return redirect(index)
