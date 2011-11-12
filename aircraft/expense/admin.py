from django.contrib import admin
from forms import DirectExpenseForm

from aircraft.expense.models import (Flight, Expense, ExpenseCategory, DirectExpense, VariableExpense, 
                                     FixedExpense, ExpenseResponsibility, Payment, FlightResponsibility)

class FlightResponsibilityInline(admin.TabularInline):
    model = FlightResponsibility
    
class FlightAdmin(admin.ModelAdmin):
    inlines = [
        FlightResponsibilityInline,
        ]


class PaymentInline(admin.TabularInline):
    model = Payment

    class Meta:
        verbose_name = u"Pagamento"
        verbose_name_plural = u"Pagamentos"
    
class ExpenseResponsibilityInline(admin.TabularInline):
    model = ExpenseResponsibility
    
class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass

class DirectExpenseAdmin(admin.ModelAdmin):
    form = DirectExpenseForm
    inlines = [
        PaymentInline,
        ]


class VariableExpenseAdmin(admin.ModelAdmin):
    pass

class FixedExpenseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flight, FlightAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, DirectExpenseAdmin)
admin.site.register(FixedExpense, VariableExpenseAdmin)
