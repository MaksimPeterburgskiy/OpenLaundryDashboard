
from .models import LaundryMachine, Kasa, KasaPowerReading
import asyncio
from kasa import SmartPlug


def pollKasaDevices():
    
    for switch in Kasa.objects.all():
            p = SmartPlug(switch.ip_address)
            asyncio.run(p.update())  # Request the update
            KasaPowerReading.objects.create(kasa=switch, 
                                            current=p.emeter_realtime['current'], 
                                            voltage=p.emeter_realtime['voltage'], 
                                            power=p.emeter_realtime['power'])
            print("Kasa: " + switch.ip_address + " - " + str(p.emeter_realtime['power']))
            
        