# -*- coding: utf-8 -*-

from django.contrib import admin

from flight.models import PAX, Flight

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'system_user', 'owner')

class PAXInline(admin.TabularInline):
    model = PAX
    extra = 2
    
class FlightAdmin(admin.ModelAdmin):
    inlines = [
        PAXInline,
        ]

#admin.site.register(Person, PersonAdmin)
admin.site.register(Flight, FlightAdmin)
