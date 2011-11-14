# -*- coding: utf-8 -*-

from models import do_calculations
class CalculatorMiddleware(object):

    def process_response(self, request, response):
        do_calculations()
        return response
