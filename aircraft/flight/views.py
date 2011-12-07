# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Sum

from flight.models import Flight


def status(request):
    try:
        hobbs = Flight.objects.all().order_by('-number')[0].end_hobbs
        cycles = Flight.objects.aggregate(Sum('cycles'))['cycles__sum']
    except IndexError:
        #Não há nenhum vôo
        hobbs = 0
        cycles = 0

    return render_to_response('status.html',
                              { 'hobbs': hobbs, 'cycles': cycles },
                              context_instance=RequestContext(request))

 

