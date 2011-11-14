from django.contrib import admin
from admin_tools.dashboard import Dashboard

from forms import DirectExpenseForm, VariableExpenseForm, FixedExpenseForm

from aircraft.expense.models import * #(Flight, Expense, ExpenseCategory, DirectExpense, VariableExpense, 
                                      #FixedExpense, Responsibility, Payment, PAX)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'system_user', 'owner')

# Flight

class PAXInline(admin.TabularInline):
    model = PAX
    extra = 2
    
class FlightAdmin(admin.ModelAdmin):
    inlines = [
        PAXInline,
        ]

# Expenses

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'expense_type')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    prepopulated_fields = {'ammount': ('ammount',) }

    class Meta:
        verbose_name = u"Pagamento"
        verbose_name_plural = u"Pagamentos"

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('ammount', 'date', 'type_name', 'category_name', 'child', 'responsibility')
    list_filter = ('date', 'category')
    search_fields = ('ammount',)

    inlines = [
        PaymentInline,
        ]

    def category_name(self, expense):
        try:
            return expense.category.name
        except AttributeError:
            return '-'
    category_name.short_description = 'Categoria'

    def type_name(self, expense):
        return self.expense(expense).__class__._meta.verbose_name

    type_name.short_description = 'Tipo de despesa'
    
class DirectExpenseAdmin(ExpenseAdmin):
    list_display = ( 'ammount', 'date', 'flight', 'responsibility' )
    list_filter = ('date', 'category')
    form = DirectExpenseForm

class VariableExpenseAdmin(ExpenseAdmin):
    list_display = ( 'ammount', 'date', 'start', 'end', 'responsibility' )
    list_filter = ('date', 'category')
    form = VariableExpenseForm

class FixedExpenseAdmin(ExpenseAdmin):
    list_display = ( 'ammount', 'date', 'start', 'end', 'responsibility' )
    list_filter = ('date', 'category')
    form = FixedExpenseForm

#Mantainances

class HourlyMantainanceAdmin(ExpenseAdmin):
    exclude = ('category',)
    list_filter = ('date',)

class ScheduledMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date',)

class EventualMantainanceAdmin(ExpenseAdmin):
    list_filter = ('date', 'category')

class InterpaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'by', 'to', 'ammount')


admin.site.register(Person, PersonAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(DirectExpense, DirectExpenseAdmin)
admin.site.register(VariableExpense, VariableExpenseAdmin)
admin.site.register(FixedExpense, FixedExpenseAdmin)
admin.site.register(HourlyMantainance, HourlyMantainanceAdmin)
admin.site.register(ScheduleMantainance, HourlyMantainanceAdmin)
admin.site.register(EventualMantainance, HourlyMantainanceAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Interpayment, InterpaymentAdmin)
