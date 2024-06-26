
from datetime import datetime, timedelta
import old.models
import asyncio
from kasa import SmartPlug
from discord import SyncWebhook
import aiohttp
from asgiref.sync import sync_to_async, async_to_sync
import random
from datetime import datetime
import pytz

def pollKasaDevices():
    
    for switch in old.models.Kasa.objects.all():
            try:
                p = SmartPlug(switch.ip_address)
                asyncio.run(p.update())  # Request the update
                old.models.KasaPowerReading.objects.create(kasa=switch, 
                                                current=p.emeter_realtime['current'], 
                                                voltage=p.emeter_realtime['voltage'], 
                                                power=p.emeter_realtime['power'])
                print("Kasa: " + switch.ip_address + " - " + str(p.emeter_realtime['power']))
            
            except Exception as e:
                print("Kasa: " + switch.ip_address + " - Error Reading Power " + str(e))
            
            

#remove Kasa Power Readings that are older than 30 days
def cleanupKasaReadings():
    
    print(old.models.KasaPowerReading.objects.filter(timestamp__lte=datetime.now() - timedelta(days=30)).delete())
    
    print("Kasa Power Readings Cleaned Up")


def sendDiscordNotification(machine):   
    # get hook used for machine (Many to Many)
    hooks = machine.discordhook_set.all()
    for hook in hooks:
        # create a webhook
        webhook = SyncWebhook.from_url(hook.webhook_url)
        # compose message content
        content = hook.ping_tag + " " + machine.name + " " + machine.get_machine_type_display() + " is now " + machine.get_status_display() + "! ("+ str(datetime.now(pytz.timezone("America/New_York")).strftime("%a %b %d %I:%M%p"))+ ")"
        # if the hook doesn't have a message id, send a new message
        if not hook.message_id:
            message = webhook.send(content, username=hook.discord_name, avatar_url=hook.avatar_url, wait=True)
            # get message id from received message and save it to the hook model
            hook.message_id = message.id
            hook.save()

        # else edit the existing message
        else:
            # check if message still exists, delete and send new message
            try:
                webhook.delete_message(hook.message_id)
            except:
                pass
            message = webhook.send(content, username=hook.discord_name, avatar_url=hook.avatar_url, wait=True)
            # get message id
            hook.message_id = message.id
            hook.save()

        
        