# -*- coding: utf-8 -*-

from django.contrib import admin

from flight.models import PAX, Flight, Person, Outage
from flight.forms import FlightForm

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'system_user', 'owner')

class PAXInline(admin.TabularInline):
    model = PAX
    extra = 2
    
class FlightAdmin(admin.ModelAdmin):
    form = FlightForm
    inlines = [
        PAXInline,
        ]

class OutageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flight, FlightAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Outage, OutageAdmin)
