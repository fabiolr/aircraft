# -*- coding: utf-8 -*-

from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from flight.models import Flight, Airport

class ViewTest(TestCase):

    def setUp(self):
        Airport.objects.create(icao='AAAA', remote_id=1, latitude=0, longitude=0)
        Airport.objects.create(icao='BBBB', remote_id=2, latitude=0, longitude=0)
        Airport.objects.create(icao='CCCC', remote_id=3, latitude=0, longitude=0)
        Airport.objects.create(icao='DDDD', remote_id=4, latitude=0, longitude=0)
        
        user = User.objects.create_user('user', 'testuser@hacklab.com.br', 'user')
        user.is_superuser = False
        user.save()


    def test_status_shows_total_cycles_and_current_hobbs(self):
        client = Client()

        resp = client.get('/status/')

        self.assertEquals(200, resp.status_code)
        self.assertEquals(resp.context['hobbs'], 0)
        self.assertEquals(resp.context['cycles'], 0)

        Flight.objects.create(start_hobbs=0,
                              origin=Airport.objects.get(icao='AAAA'),
                              destiny=Airport.objects.get(icao='BBBB'),
                              end_hobbs=5,
                              cycles=1,
                              date=date(2011, 11, 15))
        

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(resp.context['hobbs'], 5)
        self.assertEquals(resp.context['cycles'], 1)


        flight2 = Flight.objects.create(start_hobbs=5,
                                        end_hobbs=10,
                                        origin=Airport.objects.get(icao='BBBB'),
                                        destiny=Airport.objects.get(icao='CCCC'),
                                        cycles=2,
                                        date=date(2011, 11, 16))

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(resp.context['hobbs'], 10)
        self.assertEquals(resp.context['cycles'], 3)

        flight2.delete()

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(resp.context['hobbs'], 5)
        self.assertEquals(resp.context['cycles'], 1)
        
        flight2 = Flight.objects.create(start_hobbs=5,
                                        end_hobbs=9.5,
                                        origin=Airport.objects.get(icao='BBBB'),
                                        destiny=Airport.objects.get(icao='CCCC'),
                                        cycles=1,
                                        date=date(2011, 11, 16))

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertAlmostEquals(resp.context['hobbs'], 9.5)
        self.assertEquals(resp.context['cycles'], 2)
        
