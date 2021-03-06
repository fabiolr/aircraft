# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from flight.models import Person, Flight, Outage, Airport, OperationalBase
from expense.models import (DirectExpense, VariableExpense, FixedExpense,
                            HourlyMantainance, ScheduleMantainance, EventualMantainance)
from finance.models import (Interpayment, Expense, Responsibility,
                            calculate_interpayments, do_calculations, trigger_calculation)

from . import dev, set_ammount
from fixtures import fixtures_3_return_flights_in_3_months

class TestDirectExpense(TestCase):

    def setUp(self):
        self.a = Airport.objects.create(icao='ABCD', remote_id=1, latitude=0, longitude=0)
        self.b = Airport.objects.create(icao='DCBA', remote_id=2, latitude=0, longitude=0)
        self.c = Airport.objects.create(icao='AEIO', remote_id=3, latitude=0, longitude=0)
        self.d = Airport.objects.create(icao='AEIU', remote_id=4, latitude=0, longitude=0)
        self.o = Airport.objects.create(icao='SBJD', remote_id=5, latitude=0, longitude=0)
        OperationalBase.objects.create(base=self.o)

    def test_responsibility_is_shared_proportional_to_pax(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date=date(2011, 11, 12),
                                       origin=self.o,
                                       destiny=self.a,
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
                                               )
        set_ammount(expense, 1600)

        responsibility = expense.responsibility_set.all()
      
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 1000)

        set_ammount(expense, 1200)
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
                                       origin=self.o,
                                       destiny=self.a,
                                       start_hobbs=100,
                                       end_hobbs=200,
                                       cycles=3,
                                       mantainance=True,
                                       )

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight,
                                               )
        set_ammount(expense, 1600)


        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 800)
        self.assertEquals(responsibility[1].ammount, 800)

        set_ammount(expense, 1200)
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 600)

    
    def test_flight_responsibility_is_repeated_until_aircraft_returns_to_base(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight1 = Flight.objects.create(date=date(2011, 11, 12),
                                        origin=self.o,
                                        destiny=self.a,
                                        start_hobbs=100,
                                        end_hobbs=110,
                                        cycles=3,
                                        )

        pax1 = flight1.pax_set.create(owner=owner1,
                                      ammount=3)

        pax2 = flight1.pax_set.create(owner=owner2,
                                      ammount=5)

        flight2 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin=self.a,
                                        destiny=self.b,
                                        start_hobbs=110,
                                        end_hobbs=115,
                                        cycles=2,
                                        )
                                        

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight2,
                                               ammount=1600,
                                               )
        set_ammount(expense, 1600)
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 1000)

        flight3 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin=self.b,
                                        destiny=self.o,
                                        start_hobbs=115,
                                        end_hobbs=122,
                                        cycles=3,
                                        )

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight2,
                                               ammount=2400,
                                               )
        set_ammount(expense, 2400)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 900)
        self.assertEquals(responsibility[1].ammount, 1500)

    def test_flight_departing_base_with_no_pax_takes_responsibilities_from_next_flight(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date = date(2011, 11, 12),
                                       origin=self.o,
                                       destiny=self.c,
                                       start_hobbs=122,
                                       end_hobbs=130,
                                       cycles=3,
                                       )
        
        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight,
                                               )

        set_ammount(expense, 1600)

        self.assertTrue(not DirectExpense.objects.get(id=expense.id).calculated)
        responsibility = expense.responsibility_set.all()
        self.assertEquals(len(responsibility), 0)

        flight2 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin=self.c,
                                        destiny=self.a,
                                        start_hobbs=130,
                                        end_hobbs=131,
                                        cycles=3,
                                        )
        
        self.assertTrue(not DirectExpense.objects.get(id=expense.id).calculated)
        responsibility = expense.responsibility_set.all()
        self.assertEquals(len(responsibility), 0)

        flight3 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin=self.a,
                                        destiny=self.o,
                                        start_hobbs=131,
                                        end_hobbs=132,
                                        cycles=3,
                                        )

        pax1 = flight3.pax_set.create(owner=owner1,
                                      ammount=3)

        pax2 = flight3.pax_set.create(owner=owner2,
                                      ammount=5)

        self.assertTrue(DirectExpense.objects.get(id=expense.id).calculated)
        responsibility = expense.responsibility_set.all()
        self.assertEquals(len(responsibility), 2)

        self.assertEquals(responsibility[0].owner, owner1)
        self.assertEquals(responsibility[1].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 600)
        self.assertEquals(responsibility[1].ammount, 1000)
        
    def test_base_can_be_changed(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        # First, we fly from base to A, then back to base. 
        # All responsibility from Owner 1

        flight1 = Flight.objects.create(date=date(2011, 11, 12),
                                        origin=self.o,
                                        destiny=self.a,
                                        start_hobbs=100,
                                        end_hobbs=110,
                                        cycles=3,
                                        )

        flight1.pax_set.create(owner=owner1, ammount=5)

        flight2 = Flight.objects.create(date = date(2011, 11, 12),
                                        origin=self.a,
                                        destiny=self.o,
                                        start_hobbs=110,
                                        end_hobbs=115,
                                        cycles=2,
                                        )

        flight2.pax_set.create(owner=owner1, ammount=5)
                                        
        # Now, mantainance flight to C, that becomes new base

        flight3 = Flight.objects.create(date=date(2011,11,13),
                                        origin=self.o,
                                        destiny=self.c,
                                        start_hobbs=115,
                                        end_hobbs=120,
                                        cycles=1,
                                        mantainance=True)

        OperationalBase.objects.create(since=flight3, base=self.c)

        # Flight 4 goes from new base with pax from owner 2

        flight4 = Flight.objects.create(date=date(2011,11,14),
                                        origin=self.c,
                                        destiny=self.d,
                                        start_hobbs=120,
                                        end_hobbs=121,
                                        cycles=1)

        flight4.pax_set.create(owner=owner2, ammount=1)

        # Flight 5 returns to new base empty.
        # Owner2 must be fully responsible for all its expenses

        flight5 = Flight.objects.create(date=date(2011,11,15),
                                        origin=self.d,
                                        destiny=self.c,
                                        start_hobbs=121,
                                        end_hobbs=122,
                                        cycles=1)
                                       
        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight5,
                                               ammount=1600,
                                               )
        set_ammount(expense, 1600)
        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 1)
        self.assertEquals(responsibility[0].owner, owner2)
        self.assertEquals(responsibility[0].ammount, 1600)

    def test_payment_deletion_will_leave_no_resposibility(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight1 = Flight.objects.create(date=date(2011, 11, 12),
                                        origin=self.o,
                                        destiny=self.a,
                                        start_hobbs=100,
                                        end_hobbs=110,
                                        cycles=3,
                                        )

        flight1.pax_set.create(owner=owner1, ammount=1)
        flight1.pax_set.create(owner=owner2, ammount=1)

        expense = DirectExpense.objects.create(date=date(2011, 11, 12),
                                               flight=flight1,
                                               ammount=200,
                                               )

        expense.payment_set.create(paid_by=owner1, ammount=200)
        
        expense.payment_set.all()[0].delete()

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(responsibility[0].ammount, 0)
        self.assertEquals(responsibility[1].ammount, 0)

class VariableExpenseTest(TestCase):

    """
    Two flights in October, only owner 1, 20 hobbs
    Two flights in November, only owner 2, 20 hobbs
    Two flights in December, owner 2 has twice the PAX of owner1, 60 hobbs

    Each flight goes on day 12 and return on 13

    On December 20 it goes to mantainance and back, 4 hobbs
    
    """

    def setUp(self):
        fixtures_3_return_flights_in_3_months()    
    
    @dev
    def test_only_considers_given_period(self):
        # Only second flight
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 11, 30),
                                                 date=date(2011, 12, 15),
                                                 ammount=1500,
                                                 )
        set_ammount(expense, 1500)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 1)
        self.assertEquals(responsibility[0].owner.id, 2)
        self.assertEquals(responsibility[0].ammount, 1500)

    
    def test_considers_total_pax_over_all_flights(self):
        # First and second flight, should be equally distributed
        expense = VariableExpense.objects.create(start=date(2011, 10, 1),
                                                 end=date(2011, 11, 30),
                                                 date=date(2011, 12, 15),
                                                 ammount=1500,
                                                 )
        set_ammount(expense, 1500)

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
        set_ammount(expense, 1500)
        
        responsibility = expense.responsibility_set.all()

        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 1000)


    def test_considers_hobbs_of_each_flight(self):
        # second and third flights
        # second is 20 hobbs, only owner 2
        # third is 60 hobbs, and owner 2 has twice PAX
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 12, 15),
                                                 date=date(2011, 12, 15),
                                                 )
        set_ammount(expense, 800)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 600)

    def test_mantainance_is_shared_equally(self):
        # The two way flight for mantainances
        expense = VariableExpense.objects.create(start=date(2011, 12, 18),
                                                 end=date(2011, 12, 22),
                                                 date=date(2011, 12, 25),
                                                 ammount=100,
                                                 )
        set_ammount(expense, 100)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 50)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 50)


        # Now the two flights, going and returning, one for mantainance
        
        expense = VariableExpense.objects.create(start=date(2011, 12, 1),
                                                 end=date(2011, 12, 22),
                                                 date=date(2011, 12, 25),
                                                 ammount=6400,
                                                 )
        set_ammount(expense, 6400)

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
        set_ammount(expense, 3400)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2200)


class FixedExpenseTest(TestCase):

    def setUp(self):
        OperationalBase.objects.create(base=Airport.objects.create(icao='SBJD'))

    def test_expenses_are_shared_equally_no_matter_flights(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date=date(2011, 11, 12),
                                       origin=Airport.objects.get_or_create(icao='SBJD')[0],
                                       destiny=Airport.objects.get_or_create(icao='ABCD')[0],
                                       start_hobbs=100,
                                       end_hobbs=200,
                                       cycles=3,
                                       )

        flight.pax_set.create(owner=owner1, ammount=10)

        expense = FixedExpense.objects.create(start=date(2011, 11, 1),
                                              end=date(2011, 11, 30),
                                              date=date(2011, 12, 1),
                                              ammount=1000,
                                              )
        set_ammount(expense, 1000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 500)

class HourlyMantainanceTest(TestCase):
    
    def setUp(self):
        fixtures_3_return_flights_in_3_months()    
    
    def test_only_considers_desired_hobbs_interval(self):
        # Second flight
        # Second flight is 140-170 hobbs, so it will be fully considered.
        # There are 60 hobbs being considered, user 1 pays for 20 and 2 for 40
        
        expense = HourlyMantainance.objects.create(hobbs=200,
                                                   hours=50,
                                                   date=date(2011, 12, 25),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=6000,
                                                   )
        set_ammount(expense, 6000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 2000)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 4000)

    
    def test_considers_total_pax_over_all_flights(self):
        # First and second flight, should be equally distributed
        expense = HourlyMantainance.objects.create(hobbs=140,
                                                   hours=40,
                                                   date=date(2011, 12, 15),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=1500,
                                                   )
        set_ammount(expense, 1500)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 750)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 750)

        # Only third flight
        expense = HourlyMantainance.objects.create(hobbs=200,
                                                   hours=60,
                                                   date=date(2011, 12, 15),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=1500,
                                                   )
        set_ammount(expense, 1500)
        
        responsibility = expense.responsibility_set.all()

        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 1000)


    def test_considers_hobbs_of_each_flight(self):
        # second and third flights
        # second is 20 hobbs, only owner 2
        # third is 60 hobbs, and owner 2 has twice PAX
        expense = HourlyMantainance.objects.create(hobbs=200,
                                                   hours=80,
                                                   date=date(2011, 12, 15),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=800,
                                                   )
        set_ammount(expense, 800)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 600)

    def test_mantainance_is_shared_equally(self):
        # All three flights considered, plus one way to mantainance
        # 102 hobbs total. 1 pays for 41 and 2 for 62
        expense = HourlyMantainance.objects.create(hobbs=202,
                                                   hours=100,
                                                   date=date(2011, 12, 25),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=10200,
                                                   )
        set_ammount(expense, 10200)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 4100)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 6100)


    def test_return_flight_considers_pax_of_last_flight(self):
        expense = HourlyMantainance.objects.create(hobbs=200,
                                                   hours=30,
                                                   date=date(2011, 12, 22),
                                                   mantainance_date=date(2011,12,23),
                                                   ammount=3000,
                                                   )
        set_ammount(expense, 3000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1000)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2000)

    def test_if_there_are_no_flights_accounts_shared_equally(self):
        # Mostly during tests
        expense = HourlyMantainance.objects.create(hobbs=1000,
                                                   hours=100,
                                                   date=date(2012, 12, 25),
                                                   mantainance_date=date(2012,12,23),
                                                   ammount=6000,
                                                   )
        set_ammount(expense, 6000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 3000)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 3000)

        
class ScheduleMantainanceTest(TestCase):
    def setUp(self):
        fixtures_3_return_flights_in_3_months()    
    
    
    def test_only_considers_given_period(self):
        # Only second flight
        expense = ScheduleMantainance.objects.create(period=30,#2011, 11, 1),
                                                     mantainance_date=date(2011, 11, 30),
                                                     date=date(2011, 12, 15),
                                                     ammount=1500,
                                                     )
        set_ammount(expense, 1500)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 1)
        self.assertEquals(responsibility[0].owner.id, 2)
        self.assertEquals(responsibility[0].ammount, 1500)

    
    def test_considers_total_pax_over_all_flights(self):
        # First and second flight, should be equally distributed
        expense = ScheduleMantainance.objects.create(period=60,#2011, 10, 1),
                                                     mantainance_date=date(2011, 11, 30),
                                                     date=date(2011, 12, 15),
                                                     ammount=1500,
                                                     )
        set_ammount(expense, 1500)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 750)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 750)

        # Only third flight
        expense = ScheduleMantainance.objects.create(period=15,#2011, 12, 1),
                                                     mantainance_date=date(2011, 12, 15),
                                                     date=date(2011, 12, 15),
                                                     ammount=1500,
                                                     )
        set_ammount(expense, 1500)
        
        responsibility = expense.responsibility_set.all()

        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 1000)


    def test_considers_hobbs_of_each_flight(self):
        # second and third flights
        # second is 20 hobbs, only owner 2
        # third is 60 hobbs, and owner 2 has twice PAX
        expense = ScheduleMantainance.objects.create(period=45,#2011, 11, 1),
                                                     mantainance_date=date(2011, 12, 15),
                                                     date=date(2011, 12, 15),
                                                     ammount=800,
                                                     )
        set_ammount(expense, 800)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 600)

    def test_mantainance_is_shared_equally(self):
        # The two way flight for mantainances
        expense = ScheduleMantainance.objects.create(period=4,#2011, 12, 18),
                                                     mantainance_date=date(2011, 12, 22),
                                                     date=date(2011, 12, 25),
                                                     ammount=100,
                                                     )
        set_ammount(expense, 100)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 50)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 50)


        # Now the two flights, going and returning, one for mantainance
        
        expense = ScheduleMantainance.objects.create(period=22,#2011, 12, 1),
                                                     mantainance_date=date(2011, 12, 22),
                                                     date=date(2011, 12, 25),
                                                     ammount=6400,
                                                     )
        set_ammount(expense, 6400)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 2200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 4200)

    
    def test_return_flight_considers_pax_of_last_flight(self):
        expense = ScheduleMantainance.objects.create(period=9,#2011, 12, 13),
                                                     mantainance_date=date(2011, 12, 22),
                                                     date=date(2011, 12, 22),
                                                     ammount=3400,
                                                     )
        set_ammount(expense, 3400)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2200)


class EventualMantainanceTest(TestCase):
    
    def setUp(self):
        OperationalBase.objects.create(base=Airport.objects.create(icao='SBJD'))

    def test_if_there_is_responsible_than_he_pays_for_all(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        outage = Outage.objects.create(discovery_date=date(2011, 12, 22),
                                       responsible=owner1,
                                       cause='Unknown')

        expense = EventualMantainance.objects.create(outage=outage,
                                                     date=date(2011, 12, 22),
                                                     ammount=5000,
                                                     )
        set_ammount(expense, 5000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 1)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 5000)

    def test_if_there_is_no_responsible_bill_is_shared(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        outage = Outage.objects.create(discovery_date=date(2011, 12, 22),
                                       cause='Unknown')
        
        expense = EventualMantainance.objects.create(outage=outage,
                                                     date=date(2011, 12, 22),
                                                     ammount=5000,
                                                     )
        set_ammount(expense, 5000)

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 2500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2500)


class InterpaymentCalculationTest(TestCase):

    def setUp(self):
        OperationalBase.objects.create(base=Airport.objects.create(icao='SBJD'))

    def test_no_interpayments_are_required_when_there_are_no_debts(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 13))
        ex.payment_set.create(ammount=500, paid_by=o1)
        ex.payment_set.create(ammount=500, paid_by=o2)
        ex.responsibility_set.create(ammount=500, owner=o1)
        ex.responsibility_set.create(ammount=500, owner=o2)
        
        self.assertEquals(len(calculate_interpayments()), 0)

    def test_one_owes_all_to_other(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 13))
        ex.payment_set.create(ammount=1000, paid_by=o2)
        ex.responsibility_set.create(ammount=1000, owner=o1)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o1, o2, 1000))

    def test_one_pays_for_both(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 13))
        ex.payment_set.create(ammount=1000, paid_by=o2)
        ex.responsibility_set.create(ammount=500, owner=o1)
        ex.responsibility_set.create(ammount=500, owner=o2)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o1, o2, 500))

    def test_mixed_still_one_payment(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 13))
        ex.payment_set.create(ammount=900, paid_by=o1)
        ex.payment_set.create(ammount=100, paid_by=o2)
        ex.responsibility_set.create(ammount=300, owner=o1)
        ex.responsibility_set.create(ammount=700, owner=o2)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o2, o1, 600))

    def test_previous_interpayments_are_considered_in_calculation(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=900, paid_by=o1)
        ex.payment_set.create(ammount=100, paid_by=o2)
        ex.responsibility_set.create(ammount=300, owner=o1)
        ex.responsibility_set.create(ammount=700, owner=o2)

        Interpayment.objects.create(date=date(2011, 11, 13), by=o2, to=o1, ammount=300)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o2, o1, 300))

    def test_two_payments_involved(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=900, paid_by=o1)
        ex.payment_set.create(ammount=100, paid_by=o2)
        ex.responsibility_set.create(ammount=300, owner=o1)
        ex.responsibility_set.create(ammount=700, owner=o2)

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=2000, paid_by=o2)
        ex.responsibility_set.create(ammount=1000, owner=o1)
        ex.responsibility_set.create(ammount=1000, owner=o2)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o1, o2, 400))
        
        Interpayment.objects.create(date=date(2011, 11, 13), by=o1, to=o2, ammount=300)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o1, o2, 100))
        
        Interpayment.objects.create(date=date(2011, 11, 13), by=o1, to=o2, ammount=100)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 0)
        
    def test_two_payments_involved(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)
        p1 = Person.objects.create(name=u'Pilot')

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=900, paid_by=o1)
        ex.payment_set.create(ammount=100, paid_by=o2)
        ex.responsibility_set.create(ammount=300, owner=o1)
        ex.responsibility_set.create(ammount=700, owner=o2)

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=100, paid_by=p1)
        ex.responsibility_set.create(ammount=50, owner=o1)
        ex.responsibility_set.create(ammount=50, owner=o2)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 2)
        self.assertTrue((o2, o1, 550) in payments)
        self.assertTrue((o2, p1, 100) in payments)

        # pilot is paid by o1 instead of 02
        Interpayment.objects.create(date=date(2011, 11, 13), by=o1, to=p1, ammount=100)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 1)
        self.assertEquals(payments[0], (o2, o1, 650))
        
        Interpayment.objects.create(date=date(2011, 11, 13), by=o2, to=o1, ammount=650)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 0)

    def test_interpayments_are_calculated_when_one_expense_is_created(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = FixedExpense.objects.create(date=date(2011, 11, 13),
                                         start=date(2011, 10, 1),
                                         end=date(2011,11,1))
        ex.payment_set.create(ammount=1000, paid_by=o2)

        do_calculations()

        self.assertEquals(Interpayment.objects.filter(paid=True).count(), 0)
        self.assertEquals(Interpayment.objects.filter(paid=False).count(), 1)

        pay = Interpayment.objects.all()[0]
        self.assertEquals(pay.by, o1)
        self.assertEquals(pay.to, o2)
        self.assertEquals(pay.ammount, 500)

    def test_interpayments_are_calculated_when_one_expense_is_deleted(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        ex = FixedExpense.objects.create(date=date(2011, 11, 13),
                                         start=date(2011, 10, 1),
                                         end=date(2011,11,1))
        ex.payment_set.create(ammount=1000, paid_by=o2)

        do_calculations()

        ex.delete()

        do_calculations()

        self.assertEquals(Interpayment.objects.filter().count(), 0)

    def test_non_calculated_expenses_are_ignored_on_interpayments_calculations(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date = date(2011, 11, 12),
                                       origin=Airport.objects.get_or_create(icao='SBJD')[0],
                                       destiny=Airport.objects.get_or_create(icao='AEIO')[0],
                                       start_hobbs=122,
                                       end_hobbs=130,
                                       cycles=3,
                                       )
        
        ex = DirectExpense.objects.create(date=date(2011, 11, 12),
                                          flight=flight,
                                          )
        ex.payment_set.create(ammount=500, paid_by=o1)

        assert ex.calculated == False
        
        do_calculations()

        self.assertEquals(Interpayment.objects.all().count(), 0)

    def test_cents_and_float_precision(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)
        p1 = Person.objects.create(name=u'Pilot')

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=900, paid_by=o1)
        ex.payment_set.create(ammount=100, paid_by=o2)
        ex.responsibility_set.create(ammount=300, owner=o1)
        ex.responsibility_set.create(ammount=700, owner=o2)

        ex = Expense.objects.create(date=date(2011, 11, 12))
        ex.payment_set.create(ammount=100.01, paid_by=p1)
        ex.responsibility_set.create(ammount=50, owner=o1)
        ex.responsibility_set.create(ammount=50.01, owner=o2)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 2)
        self.assertTrue((o2, o1, 550) in payments)
        self.assertTrue((o2, p1, 100.01) in payments)

        # pilot is paid by o1 instead of 02
        Interpayment.objects.create(date=date(2011, 11, 13), by=o1, to=p1, ammount=100)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 2)
        self.assertTrue((o2, o1, 650) in payments)
        self.assertTrue((o2, p1, .01) in payments)

        Interpayment.objects.create(date=date(2011, 11, 13), by=o2, to=o1, ammount=650)
        Interpayment.objects.create(date=date(2011, 11, 13), by=o2, to=p1, ammount=.01)

        payments = calculate_interpayments()
        self.assertEquals(len(payments), 0)

    def test_calculations_turn_trigger_off(self):
        o1 = Person.objects.create(name=u'Owner 1', owner=True)
        o2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date = date(2011, 11, 12),
                                       origin=Airport.objects.get_or_create(icao='SBJD')[0],
                                       destiny=Airport.objects.get_or_create(icao='AEIO')[0],
                                       start_hobbs=122,
                                       end_hobbs=130,
                                       cycles=3,
                                       mantainance=True,
                                       )
        
        ex = DirectExpense.objects.create(date=date(2011, 11, 12),
                                          flight=flight,
                                          )
        ex.payment_set.create(ammount=1000, paid_by=o1)


        self.assertTrue(Interpayment.triggered)

        do_calculations()

        self.assertTrue(not Interpayment.triggered)
        

 
