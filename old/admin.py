from django.contrib import admin


#laundry machine
from .models import LaundryMachine, Kasa, KasaPowerReading

admin.site.register(LaundryMachine)
admin.site.register(Kasa)
admin.site.register(KasaPowerReading)
