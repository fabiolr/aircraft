# -*- coding: utf-8 -*-

from django.contrib import admin

from finance.models import Interpayment, Payment, Expense

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    prepopulated_fields = {'ammount': ('ammount',) }

    class Meta:
        verbose_name = u"Pagamento"
        verbose_name_plural = u"Pagamentos"

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('ammount', 'date', 'type_name', 'category_name', 'child', 'responsibility', 'checked')
    list_filter = ('date', 'category')
    search_fields = ('ammount',)
    list_display_links = ()

    inlines = [
        PaymentInline,
        ]

    def get_readonly_fields(self, request, instance=None):
        if request.user.is_superuser:
            return []
        return ['checked']

    def category_name(self, expense):
        try:
            return expense.category.name
        except AttributeError:
            return '-'
    category_name.short_description = 'Categoria'

    def type_name(self, expense):
        return self.expense(expense).__class__._meta.verbose_name

    type_name.short_description = 'Tipo de despesa'
    
class InterpaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'by', 'to', 'ammount')

try:
    admin.site.register(Interpayment, InterpaymentAdmin)
    admin.site.register(Expense, ExpenseAdmin)
except:
    pass



