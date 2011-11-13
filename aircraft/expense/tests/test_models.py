# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from expense.models import (Person, Expense, Responsibility, Flight,
                            DirectExpense, VariableExpense, FixedExpense,
                            HourlyMantainance, ScheduleMantainance, EventualMantainance,
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
        # second is 20 hobbs, only owner 2
        # third is 60 hobbs, and owner 2 has twice PAX
        expense = VariableExpense.objects.create(start=date(2011, 11, 1),
                                                 end=date(2011, 12, 15),
                                                 date=date(2011, 12, 15),
                                                 ammount=800,
                                                 )

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


class FixedExpenseTest(TestCase):

    def test_expenses_are_shared_equally_no_matter_flights(self):
        owner1 = Person.objects.create(name=u'Owner 1', owner=True)
        owner2 = Person.objects.create(name=u'Owner 2', owner=True)

        flight = Flight.objects.create(date=date(2011, 11, 12),
                                       origin='SBJD',
                                       destiny='ABCD',
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

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 500)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 500)

class HourlyMantainanceTest(TestCase):
    
    fixtures = ['3_return_flights_in_3_months.json']
    
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

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1000)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2000)

class ScheduleMantainanceTest(TestCase):
    fixtures = ['3_return_flights_in_3_months.json']
    
    
    def test_only_considers_given_period(self):
        # Only second flight
        expense = ScheduleMantainance.objects.create(period=30,#2011, 11, 1),
                                                     mantainance_date=date(2011, 11, 30),
                                                     date=date(2011, 12, 15),
                                                     ammount=1500,
                                                     )

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

        responsibility = expense.responsibility_set.all()
        
        self.assertEquals(len(responsibility), 2)
        self.assertEquals(responsibility[0].owner.id, 1)
        self.assertEquals(responsibility[0].ammount, 1200)
        self.assertEquals(responsibility[1].owner.id, 2)
        self.assertEquals(responsibility[1].ammount, 2200)


