from django.contrib import admin
from forms import DirectExpenseForm, VariableExpenseForm, FixedExpenseForm

from aircraft.expense.models import * #(Flight, Expense, ExpenseCategory, DirectExpense, VariableExpense, 
                                      #FixedExpense, Responsibility, Payment, PAX)

class PersonAdmin(admin.ModelAdmin):
    pass

# Flight

class PAXInline(admin.TabularInline):
    model = PAX
    
class FlightAdmin(admin.ModelAdmin):
    inlines = [
        PAXInline,
        ]

# Expenses

class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass


class PaymentInline(admin.TabularInline):
    model = Payment

    class Meta:
        verbose_name = u"Pagamento"
        verbose_name_plural = u"Pagamentos"

class ExpenseAdmin(admin.ModelAdmin):
    inlines = [
        PaymentInline,
        ]
    
class DirectExpenseAdmin(ExpenseAdmin):
    form = DirectExpenseForm

class VariableExpenseAdmin(ExpenseAdmin):
    form = VariableExpenseForm

class FixedExpenseAdmin(ExpenseAdmin):
    form = FixedExpenseForm

#Mantainances

class HourlyMantainanceAdmin(ExpenseAdmin):
    exclude = ('category',)
    pass

class ScheduledMantainanceAdmin(ExpenseAdmin):
    pass

class EventualMantainanceAdmin(ExpenseAdmin):
    pass



admin.site.register(Person, PersonAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, DirectExpenseAdmin)
admin.site.register(FixedExpense, VariableExpenseAdmin)
admin.site.register(HourlyMantainance, HourlyMantainanceAdmin)
admin.site.register(ScheduleMantainance, HourlyMantainanceAdmin)
admin.site.register(EventualMantainance, HourlyMantainanceAdmin)
