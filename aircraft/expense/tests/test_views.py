# -*- coding: utf-8 -*-

from datetime import date
import fudge

from django.test import TestCase, Client
from django.contrib.auth.models import User

from flight.models import Person, Flight
from expense.models import DirectExpense

class DirectExpenseTest(TestCase):

    @fudge.patch('finance.models.do_calculations')
    def test_do_calculations_is_triggered_on_creation(self, fake_calc):
        User.objects.create_user('admin', 'testadmin@nowher.com.br', 'admin')
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date = date(2011, 11, 12),
                                       origin='SBJD',
                                       destiny='AEIO',
                                       start_hobbs=122,
                                       end_hobbs=130,
                                       cycles=3,
                                       )

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight,
                                               )
        expense.payment_set.create(paid_by=o1, ammount=500)
        
        
        client = Client()
        client.login(username='admin', password='admin')

        fake_calc.expects_call()

        client.post('/admin/expense/directexpense/add/', { 'date': '2011-11-15',
                                                           'category': 6,
                                                           'flight': flight.id,
                                                           'description': 'test',
                                                           'payment_set-0-paid_by': o1.id,
                                                           'payment_set-0-ammount': 1000,
                                                           })
                                                           
