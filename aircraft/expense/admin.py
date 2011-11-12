from django.contrib import admin
from forms import DirectExpenseForm, VariableExpenseForm, FixedExpenseForm

from aircraft.expense.models import (Flight, Expense, ExpenseCategory, DirectExpense, VariableExpense, 
                                     FixedExpense, ExpenseResponsibility, Payment, FlightResponsibility)

# Flight

class FlightResponsibilityInline(admin.TabularInline):
    model = FlightResponsibility
    
class FlightAdmin(admin.ModelAdmin):
    inlines = [
        FlightResponsibilityInline,
        ]


# Expenses

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
    form = VariableExpenseForm
    inlines = [
        PaymentInline,
        ]

class FixedExpenseAdmin(admin.ModelAdmin):
    form = FixedExpenseForm
    inlines = [
        PaymentInline,
        ]

admin.site.register(Flight, FlightAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, DirectExpenseAdmin)
admin.site.register(FixedExpense, VariableExpenseAdmin)
