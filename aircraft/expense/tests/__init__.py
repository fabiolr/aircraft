# -*- coding: utf-8 -*-

from expense.models import Person
from datetime import date

def dev(test):
    test.tags = 'dev'
    return test

def set_ammount(expense, ammount):
    for pay in expense.payment_set.all():
        pay.delete()
    ghost = Person.objects.create(name="Ghost")
    expense.payment_set.create(paid_by=ghost, ammount=ammount)
