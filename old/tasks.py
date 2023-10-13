
from datetime import datetime, timedelta
import old.models
import asyncio
from kasa import SmartPlug
from discord import Webhook
import aiohttp
from asgiref.sync import sync_to_async

def pollKasaDevices():
    
    for switch in old.models.Kasa.objects.all():
            p = SmartPlug(switch.ip_address)
            asyncio.run(p.update())  # Request the update
            old.models.KasaPowerReading.objects.create(kasa=switch, 
                                            current=p.emeter_realtime['current'], 
                                            voltage=p.emeter_realtime['voltage'], 
                                            power=p.emeter_realtime['power'])
            print("Kasa: " + switch.ip_address + " - " + str(p.emeter_realtime['power']))
            

#remove Kasa Power Readings that are older than 30 days
def cleanupKasaReadings():
    
    print(old.models.KasaPowerReading.objects.filter(timestamp__lte=datetime.now() - timedelta(days=30)).delete())
    
    print("Kasa Power Readings Cleaned Up")
    
    
async def sendDiscordNotification(machine):
    
    #get hook used for machine (Many to Many)
    hooks = await sync_to_async(machine.discordhook_set.all)()
    async for hook in hooks:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(hook.webhook_url, session=session)
            await webhook.send(hook.ping_tag + " " + machine.name + " " + machine.get_machine_type_display() + " is now " + machine.get_status_display() + "!", username='LaundryBot')



    
    