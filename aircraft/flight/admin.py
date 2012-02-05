# -*- coding: utf-8 -*-

from django.contrib import admin

from flight.models import PAX, Flight, Person, Outage, OperationalBase
from flight.forms import FlightForm, PAXForm

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'system_user', 'owner')

class PAXInline(admin.TabularInline):
    form = PAXForm
    model = PAX
    extra = 2
    
class FlightAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'distance', 'speed')
    form = FlightForm
    inlines = [
        PAXInline,
        ]

class OutageAdmin(admin.ModelAdmin):
    pass

class OperationalBaseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flight, FlightAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Outage, OutageAdmin)
admin.site.register(OperationalBase, OperationalBaseAdmin)
