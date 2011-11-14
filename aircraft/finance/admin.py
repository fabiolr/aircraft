# -*- coding: utf-8 -*-

from django.contrib import admin

from finance.models import Interpayment
from expense.admin import PaymentInline

class InterpaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'by', 'to', 'ammount')

admin.site.register(Interpayment, InterpaymentAdmin)



