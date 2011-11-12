# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from expense.models import Person, Expense, Responsibility

from . import dev

class TestExpense(TestCase):

    def test_default_responsibility_is_equally_shared_among_owners(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        expense = Expense.objects.create(ammount=1000, date=date(2011, 11, 12))

        responsibility = Responsibility.objects.all()

        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].ammount, 500)

        expense.ammount = 1200
        expense.save()

        responsibility = Responsibility.objects.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 600)

        expense.delete()

        self.assertEquals(Responsibility.objects.count(), 0)

