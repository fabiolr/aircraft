# -*- coding: utf-8 -*-

from django import forms

from models import DirectExpense, VariableExpense, FixedExpense
from finance.models import ExpenseCategory
from flight.models import Flight

class DirectExpenseForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.filter(expense_type=1))
    flight = forms.ModelChoiceField(queryset=Flight.objects.all())

    def __init__(self, *args, **kwargs):
        super(DirectExpenseForm, self).__init__(*args, **kwargs)
        self.fields['flight'].queryset = Flight.objects.all() #TODO
                                    
    class Meta:
        model = DirectExpense

class VariableExpenseForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.filter(expense_type=2))
    
    class Meta:
        model = VariableExpense

class FixedExpenseForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.filter(expense_type=3))
    
    class Meta:
        model = FixedExpense
