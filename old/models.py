from django.db import models



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
    
    #avg run time in seconds
    avg_run_time = models.IntegerField(default=0)
    
    #last voltage reading
    last_voltage = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    #last current reading
    last_current = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    #last power reading
    last_power = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    
    
    #calibration settings
    on_power_threshold = models.IntegerField(default=0)
    
    #return string representation of object
    def __str__(self):
        return self.name + " " + self.get_machine_type_display() + " - " + self.get_status_display() + " - " + str(self.last_power) + "w"


     
     
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
        self.kasa.power_integration.save()
    
#-------------------------------------------------------------
