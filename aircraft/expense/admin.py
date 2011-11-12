from django.contrib import admin
from forms import DirectExpenseForm

from aircraft.expense.models import (Flight, ExpenseCategory, DirectExpense, VariableExpense, 
                                     FixedExpense)

class FlightAdmin(admin.ModelAdmin):
    pass

class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass

class DirectExpenseAdmin(admin.ModelAdmin):
    form = DirectExpenseForm
    pass

class VariableExpenseAdmin(admin.ModelAdmin):
    pass

class FixedExpenseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flight, FlightAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, DirectExpenseAdmin)
admin.site.register(FixedExpense, VariableExpenseAdmin)
