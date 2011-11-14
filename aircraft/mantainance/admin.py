# -*- coding: utf-8 -*-

from django.contrib import admin

from mantainance.models import HourlyMantainance, ScheduleMantainance, EventualMantainance
from expense.admin import ExpenseAdmin

class HourlyMantainanceAdmin(ExpenseAdmin):
    exclude = ('category',)
    list_filter = ('date',)

class ScheduledMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date',)

class EventualMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date', 'category')

admin.site.register(HourlyMantainance, HourlyMantainanceAdmin)
admin.site.register(ScheduleMantainance, HourlyMantainanceAdmin)
admin.site.register(EventualMantainance, HourlyMantainanceAdmin)
