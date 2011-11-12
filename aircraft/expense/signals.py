# -*- coding: utf-8 -*-

def calculate_expense_responsibility(sender, **kwargs):
    kwargs['instance'].share()
