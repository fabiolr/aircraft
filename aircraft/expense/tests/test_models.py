# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from expense.models import (Person, Expense, Responsibility, Flight,
                            DirectExpense, VariableExpense, FixedExpense,
                            )

from . import dev

class TestDirectExpense(TestCase):

    def test_responsibility_is_shared_proportional_to_pax(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date=date(2011, 11, 12),
                                       origin='SBJD',
                                       destiny='ABCD',
                                       start_hobbs=100,
                                       end_hobbs=200,
                                       cycles=3,
                                       )

        pax1 = flight.pax_set.create(owner=owner1,
                                     ammount=3)

        pax2 = flight.pax_set.create(owner=owner2,
                                     ammount=5)

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight,
                                               ammount=1600,
                                               )

        responsibility = expense.responsibility_set.all()
      
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 1000)

        expense.ammount = 1200
        expense.save()
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 450)
        self.assertEquals(responsibility[1].ammount, 750)

        pax1.ammount = 1
        pax1.save()
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 200)
        self.assertEquals(responsibility[1].ammount, 1000)


    def test_mantainance_flight_responsibility_is_shared_equally(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date=date(2011, 11, 12),
                                       origin='SBJD',
                                       destiny='ABCD',
                                       start_hobbs=100,
                                       end_hobbs=200,
                                       cycles=3,
                                       mantainance=True,
                                       )

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight,
                                               ammount=1600,
                                               )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 800)
        self.assertEquals(responsibility[1].ammount, 800)

        expense.ammount = 1200
        expense.save()
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 600)

    def test_fligh_responsibility_is_repeated_until_aircraft_returns_to_base(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight1 = Flight.objects.create(date=date(2011, 11, 12),
                                        origin='SBJD',
                                        destiny='ABCD',
                                        start_hobbs=100,
                                        end_hobbs=110,
                                        cycles=3,
                                        )

        pax1 = flight1.pax_set.create(owner=owner1,
                                      ammount=3)

        pax2 = flight1.pax_set.create(owner=owner2,
                                      ammount=5)

        flight2 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin='ABCD',
                                        destiny='BCDE',
                                        start_hobbs=110,
                                        end_hobbs=115,
                                        cycles=2,
                                        )
                                        

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight2,
                                               ammount=1600,
                                               )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 1000)

        flight3 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin='BCDE',
                                        destiny='SBJD',
                                        start_hobbs=115,
                                        end_hobbs=122,
                                        cycles=3,
                                        )

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight2,
                                               ammount=2400,
                                               )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 900)
        self.assertEquals(responsibility[1].ammount, 1500)

        try:
            flight4 = Flight.objects.create(date = date(2011, 11, 12),
                                            origin='SBJD',
                                            destiny='AEIO',
                                            start_hobbs=122,
                                            end_hobbs=130,
                                            cycles=3,
                                            )

            
            expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                                   flight=flight4,
                                                   ammount=1600,
                                                   )

        except ValidationError:
            pass
        else:
            self.fail("Flight departing base must have either pax or mantainance")

class VariableExpenseTest(TestCase):

    """
    Two flights in October, only owner 1, 20 hobbs
    Two flights in November, only owner 2, 20 hobbs
    Two flights in December, owner 2 has twice the PAX of owner1, 60 hobbs

    Each flight goes on day 12 and return on 13

    On December 20 it goes to mantainance and back, 4 hobbs
    
    """
    fixtures = ['3_return_flights_in_3_months.json']
    
    @dev
    def test_only_considers_given_period(self):
        # Only second flight
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 11, 30),
                                                 date=date(2011, 12, 15),
                                                 ammount=1500,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 1)
        self.assertEquals(responsibility[0].owner.id, 2)
        self.assertEquals(responsibility[0].ammount, 1500)

    @dev
    def test_considers_total_pax_over_all_flights(self):
        # First and second flight, should be equally distributed
        expense = VariableExpense.objects.create(start=date(2011, 10, 1),
                                                 end=date(2011, 11, 30),
                                                 date=date(2011, 12, 15),
                                                 ammount=1500,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 750)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 750)

        # Only third flight
        expense = VariableExpense.objects.create(start=date(2011, 12, 1),
                                                 end=date(2011, 12, 15),
                                                 date=date(2011, 12, 15),
                                                 ammount=1500,
                                                 )
        
        responsibility = expense.responsibility_set.all()

        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 1000)


    def test_considers_hobbs_of_each_flight(self):
        # second and third flights
        # second is 20 hobbs shared equally
        # third is 60 hobbs, and owner 2 has twice PAX
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 12, 15),
                                                 date=date(2011, 12, 15),
                                                 ammount=800,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 300)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 500)

    def test_mantainance_is_shared_equally(self):
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 12, 15),
                                                 date=date(2011, 12, 22),
                                                 ammount=100,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 50)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 50)


        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 12, 10),
                                                 date=date(2011, 12, 22),
                                                 ammount=6400,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 2200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 4200)


    def test_return_flight_considers_pax_of_last_flight(self):
        expense = VariableExpense.objects.create(start=date(2011, 12, 13),
                                                 end=date(2011, 12, 22),
                                                 date=date(2011, 12, 22),
                                                 ammount=3400,
                                                 )

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2200)
