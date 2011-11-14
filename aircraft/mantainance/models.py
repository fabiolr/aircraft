# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models

from expense.models import Expense, share_responsibility
from flight.models import Flight, Outage, Person

class HourlyMantainance(Expense):
    mantainance_date = models.DateField(u"Data de chegada na oficina")
    hobbs = models.FloatField(u"Hobbs de chegada na oficina")
    hours = models.IntegerField(u"Nº de horas da inspeção")
    obs = models.CharField(u"Observações", max_length=255, blank=True, null=True)

    def share(self):
        self.share_by_flights()

    @property
    def flights(self):
        return Flight.objects.filter(end_hobbs__gt=self.hobbs-self.hours) \
                             .exclude(start_hobbs__gte=self.hobbs)

    def __unicode__(self):
        return '%dH@%d, em %s' % (self.hours, self.hobbs, self.mantainance_date.strftime('%d/%m/%Y'))
    
    class Meta:
        verbose_name = u"Manutenção por hora"
        verbose_name_plural = u"Manutenções por hora"
        
models.signals.post_save.connect(share_responsibility, sender=HourlyMantainance, dispatch_uid="hmantainance")

class ScheduleMantainance(Expense):
    mantainance_date = models.DateField(u"Data de chegada na oficina")
    period = models.IntegerField(u"Período vencido em dias")

    def share(self):
        self.share_by_flights()

    @property
    def flights(self):
        start_date = self.mantainance_date - timedelta(self.period)
        return Flight.objects.filter(date__gte=start_date, date__lte=self.mantainance_date)

    def __unicode__(self):
        return '%d dias, em %s' % (self.period, self.mantainance_date.strftime('%d/%m/%Y'))

    class Meta:
        verbose_name = u"Manutenção calendárica"
        verbose_name_plural = u"Manutenções calendáricas"
    
models.signals.post_save.connect(share_responsibility, sender=ScheduleMantainance, dispatch_uid="smantainance")

class EventualMantainance(Expense):
    outage = models.ForeignKey(Outage, verbose_name=u"Pane")

    def share(self):
        if self.outage.responsible:
            self.blame(self.outage.responsible)
        else:
            self.share_equally()

    class Meta:
        verbose_name = u"Manutenção eventual"
        verbose_name_plural = u"Manuenções eventuais (Panes)"

models.signals.post_save.connect(share_responsibility, sender=EventualMantainance, dispatch_uid="emantainance")

