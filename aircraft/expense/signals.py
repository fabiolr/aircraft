# -*- coding: utf-8 -*-

def calculate_expense_responsibility(sender, **kwargs):

    from models import Expense, Person

    expense = kwargs['instance']

    for resp in expense.responsibility_set.all():
        resp.delete()

    owners = Person.objects.filter(owner=True)

    for owner in owners:
        expense.responsibility_set.create(owner=owner, ammount=expense.ammount/len(owners))
