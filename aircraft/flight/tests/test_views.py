# -*- coding: utf-8 -*-

from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from flight.models import Flight

class ViewTest(TestCase):

    def setUp(self):
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
                              origin='AAAA',
                              destiny='BBBB',
                              end_hobbs=5,
                              cycles=1,
                              date=date(2011, 11, 15))
        

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(resp.context['hobbs'], 5)
        self.assertEquals(resp.context['cycles'], 1)


        flight2 = Flight.objects.create(start_hobbs=5,
                                        end_hobbs=10,
                                        origin='BBBB',
                                        destiny='CCCC',
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
                                        origin='BBBB',
                                        destiny='CCCC',
                                        cycles=1,
                                        date=date(2011, 11, 16))

        resp = client.get('/status/')
        self.assertEquals(200, resp.status_code)
        self.assertAlmostEquals(resp.context['hobbs'], 9.5)
        self.assertEquals(resp.context['cycles'], 2)
        
