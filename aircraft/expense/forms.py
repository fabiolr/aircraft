# -*- coding: utf-8 -*-

from django import forms

from models import DirectExpense, VariableExpense, FixedExpense, ExpenseCategory

class DirectExpenseForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.filter(expense_type=1))
    
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
