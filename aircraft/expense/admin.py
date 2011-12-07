from django.contrib import admin
from admin_tools.dashboard import Dashboard

from forms import DirectExpenseForm, VariableExpenseForm, FixedExpenseForm

from expense.models import (DirectExpense, VariableExpense, FixedExpense,
                            HourlyMantainance, ScheduleMantainance, EventualMantainance)
from finance.admin import ExpenseAdmin

class DirectExpenseAdmin(ExpenseAdmin):

    list_display = ( 'br_ammount', 'date', 'flight', 'description', 'responsibility', 'checked' )
    list_filter = ('date', 'category', 'checked' )

    form = DirectExpenseForm

class VariableExpenseAdmin(ExpenseAdmin):
    list_display = ( 'br_ammount', 'date', 'start', 'end', 'responsibility', 'checked' )
    list_filter = ('date', 'category')
    form = VariableExpenseForm

class FixedExpenseAdmin(ExpenseAdmin):
    list_display = ( 'br_ammount', 'date', 'start', 'end', 'responsibility', 'checked' )
    list_filter = ('date', 'category')
    form = FixedExpenseForm

class HourlyMantainanceAdmin(ExpenseAdmin):
    exclude = ('category',)
    list_filter = ('date',)

class ScheduledMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date',)

class EventualMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date', 'category')

admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, VariableExpenseAdmin)
admin.site.register(FixedExpense, FixedExpenseAdmin)
admin.site.register(HourlyMantainance, HourlyMantainanceAdmin)
admin.site.register(ScheduleMantainance, HourlyMantainanceAdmin)
admin.site.register(EventualMantainance, HourlyMantainanceAdmin)

