import asyncio
import datetime
from django.db import models
import old.tasks
import pytz





#notification integrations

class DiscordHook(models.Model):
    webhook_name = models.CharField(max_length=200)
    machines = models.ManyToManyField('LaundryMachine')
    webhook_url = models.CharField(max_length=200)
    discord_name = models.CharField(max_length=200)
    ping_tag = models.CharField(max_length=200)
    message_id = models.CharField(max_length=200, blank=True)
    avatar_url = models.CharField(max_length=200, blank=True)
    
    
    #name
    def __str__(self):
        return self.webhook_name




#Laundry Machine (can be washer or dryer)
class LaundryMachine(models.Model):
    name = models.CharField(max_length=200)
    
    #type of machine
    MACHINE_CHOICES = [
        ("W", "Washer"),
        ("D", "Dryer"),
    ]
    machine_type = models.CharField(
        max_length=2,
        choices=MACHINE_CHOICES,
        default="W",
    )
    
    #current status of machine
    STATUS_CHOICES = [
        ("A", "Available"),
        ("R", "Running"),
        ("F", "Finished"),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="A",
    )
    
    #time when machine was last started
    last_start_time = models.DateTimeField(null=True, blank=True)
    
    #time when machine was last finished
    last_end_time = models.DateTimeField(null=True, blank=True)
    
    last_status_change_time = models.DateTimeField(null=True, blank=True)
    
    #avg run time in seconds
    avg_run_time = models.IntegerField(default=0)
    eta_minutes = models.IntegerField(default=0)
    
    #last voltage reading
    last_voltage = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    #last current reading
    last_current = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    #last power reading
    last_power = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    
    #calibration settings
    on_power_threshold = models.IntegerField(default=0)
    
    #return string representation of object
    def __str__(self):
        return self.name + " " + self.get_machine_type_display() + " - " + self.get_status_display() + " - " + str(self.last_power) + "w"

    def save(self, *args, **kwargs):
        super(LaundryMachine, self).save(*args, **kwargs)
        #if machine status set to available, send a Notification
        if(self.status == "A"):
            old.tasks.sendDiscordNotification(self)

    def machine_type_string(self):
        return self.get_machine_type_display()
    def machine_status_string(self):
        return self.get_status_display()
    def machine_last_status_change_time_string(self):
    # format Tue Oct 31 4:43pm in new york time (not -4)
        return self.last_status_change_time.astimezone(pytz.timezone("America/New_York")).strftime("%a %b %-d %-I:%M %p") 
#Kasa Module Specific 
#-------------------------------------------------------------
class Kasa(models.Model):
    
    ip_address = models.CharField(max_length=200)
    mac_address = models.CharField(max_length=200)
    
    #sub model, integration to use to poll power status of machine, for now only Kasa
    power_integration = models.OneToOneField(LaundryMachine, on_delete=models.CASCADE)
    
    #return string representation of object
    def __str__(self):
        return self.ip_address + " - " + self.power_integration.name + " " + self.power_integration.get_machine_type_display()
    


#power reading
class KasaPowerReading(models.Model):
    #foreign key to kasa
    kasa = models.ForeignKey(Kasa, on_delete=models.CASCADE)
    #double precision current
    current = models.DecimalField(max_digits=10, decimal_places=3)
    #double precision Voltage
    voltage = models.DecimalField(max_digits=10, decimal_places=3)
    #double precision power
    power = models.DecimalField(max_digits=10, decimal_places=3)
    #reading timestamp
    timestamp = models.DateTimeField(auto_now=True)
    
    #return string representation of object
    def __str__(self):
        return self.kasa.ip_address + " - " + str(self.timestamp) + " - " + str(self.power)
    
    #override save to update upstream power reading
    def save(self, *args, **kwargs):
        super(KasaPowerReading, self).save(*args, **kwargs)
        self.kasa.power_integration.last_voltage = self.voltage
        self.kasa.power_integration.last_current = self.current
        self.kasa.power_integration.last_power = self.power
        
        #update eta based on avg runtime and current time
        if(self.kasa.power_integration.last_start_time is not None and self.kasa.power_integration.avg_run_time != 0):
            delta = self.kasa.power_integration.last_start_time + datetime.timedelta(minutes=self.kasa.power_integration.avg_run_time) - self.timestamp
            if delta.total_seconds() > 0:
                self.kasa.power_integration.eta_minutes = delta.seconds // 60 # convert seconds to minutes
            else:
                self.kasa.power_integration.eta_minutes = 0 # or some error handling
        change = False
        
        #set status of machine based on current power reading and power threshold
        #set to running if power is above threshold and machine is available
        if(self.power > self.kasa.power_integration.on_power_threshold and self.kasa.power_integration.status != "R"):
            if(self.kasa.power_integration.status == "A" or self.kasa.power_integration.status == "F"):
                self.kasa.power_integration.last_start_time = self.timestamp
            self.kasa.power_integration.status = "R"
            self.kasa.power_integration.last_status_change_time = self.timestamp
            change = True
            
        #set to available if power is below threshold and set end time
        elif(self.power < self.kasa.power_integration.on_power_threshold and self.kasa.power_integration.status == "R"):
            self.kasa.power_integration.status = "F"
            self.kasa.power_integration.last_end_time = self.timestamp
            self.kasa.power_integration.last_status_change_time = self.timestamp
            change = True

        #save upstream machine status
        self.kasa.power_integration.save()
        if(change):
            old.tasks.sendDiscordNotification(self.kasa.power_integration)
            
    
#-------------------------------------------------------------
