# -*- coding: utf-8 -*-

from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from flight.models import Flight

from . import dev

class FlightTest(TestCase):

    def test_number_is_always_consistently_sequential(self):
        flight1 = Flight.objects.create(start_hobbs=0,
                                        end_hobbs=10,
                                        cycles=1,
                                        date=date(2011, 11, 15))

        self.assertEquals(flight1.number, 1)

        flight2 = Flight.objects.create(start_hobbs=10,
                                        end_hobbs=11,
                                        cycles=1,
                                        date=date(2011, 11, 15))

        self.assertEquals(flight2.number, 2)

        flight2.delete()

        flight2 = Flight.objects.create(start_hobbs=10,
                                        end_hobbs=12.3,
                                        cycles=1,
                                        date=date(2011, 11, 16))

        self.assertEquals(flight2.number, 2)

    def test_hobbs_sequence_must_fit_exact_without_intersections_or_gaps(self):

        # First flight may be non-zero
        flight1 = Flight.objects.create(start_hobbs=10,
                                        end_hobbs=11.3,
                                        cycles=1,
                                        date=date(2011, 11, 15))

        try:
            Flight.objects.create(start_hobbs=11,
                                  end_hobbs=12,
                                  cycles=1,
                                  date=date(2011, 11, 16))
        except ValidationError:
            pass
        else:
            self.fail()

        try:
            Flight.objects.create(start_hobbs=11.5,
                                  end_hobbs=12,
                                  cycles=1,
                                  date=date(2011, 11, 16))
        except ValidationError:
            pass
        else:
            self.fail()

        flight2 = Flight.objects.create(start_hobbs=11.3,
                                        end_hobbs=12.5,
                                        cycles=1,
                                        date=date(2011, 11, 16))

        flight3 = Flight.objects.create(end_hobbs=13,
                                        cycles=1,
                                        date=date(2011, 11, 16))

        self.assertAlmostEquals(flight3.start_hobbs, 12.5)

        # it must be possible to save a previous flight withouth changing hobbs
        flight2.mantainance = True
        flight2.save()

    def test_start_hobbs_must_be_smaller_than_end_hobbs(self):
        try:
            Flight.objects.create(start_hobbs=10,
                                  end_hobbs=10,
                                  cycles=1,
                                  date=date(2011, 11, 15))
        except ValidationError:
            pass
        else:
            self.fail()

        try:
            Flight.objects.create(start_hobbs=10,
                                  end_hobbs=9,
                                  cycles=1,
                                  date=date(2011, 11, 15))
        except ValidationError:
            pass
        else:
            self.fail()

        try:
            Flight.objects.create(start_hobbs=-1,
                                  end_hobbs=9,
                                  cycles=1,
                                  date=date(2011, 11, 15))
        except ValidationError:
            pass
        else:
            self.fail()

    def test_flight_must_depart_from_previous_flight_destination(self):
        Flight.objects.create(start_hobbs=0,
                              end_hobbs=5,
                              origin='ABCD',
                              destiny='DCBA',
                              cycles=1,
                              date=date(2011, 11, 15))
        try:
            Flight.objects.create(start_hobbs=5,
                                  end_hobbs=6,
                                  origin='ABCD',
                                  destiny='DCBA',
                                  cycles=1,
                                  date=date(2011, 11, 16))
        except ValidationError:
            pass
        else:
            self.fail()

        flight = Flight.objects.create(start_hobbs=5,
                                       end_hobbs=6,
                                       destiny='AEIO',
                                       cycles=1,
                                       date=date(2011, 11, 16))
        self.assertEquals(flight.origin, 'DCBA')

        Flight.objects.create(start_hobbs=6,
                              end_hobbs=7,
                              origin='AEIO',
                              destiny='AEIU',
                              cycles=1,
                              date=date(2011, 11, 16))
    def test_date_of_one_flight_must_not_be_before_previous_flight(self):
        Flight.objects.create(start_hobbs=0,
                              end_hobbs=5,
                              cycles=1,
                              date=date(2011, 11, 15))
        try:
            Flight.objects.create(start_hobbs=0,
                                  end_hobbs=5,
                                  cycles=1,
                                  date=date(2011, 11, 14))
        except ValidationError:
            pass
        else:
            self.fail()
