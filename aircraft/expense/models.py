# -*- coding: utf-8 -*-

from datetime import timedelta

from django import core
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

from flight.models import Person, Flight, Outage
from finance.models import Expense, Payment

#signal
def share_responsibility(sender, **kwargs):
    if kwargs['instance'].ammount:
        kwargs['instance'].share()

class DirectExpense(Expense):
    flight = models.ForeignKey(Flight, verbose_name=u"Vôo") 
    description = models.CharField(u"Descrição", max_length=255)

    def share(self):
        try:
            self.apply_share(self.flight.responsibilities(self.ammount))
        except ValidationError:
            if self.calculated:
                self.calculated = False
                self.save() 
                # signal will be triggered again, responsibilities calculated twice
                # cruel world...

    def __unicode__(self):
        return unicode(self.flight)
        
    class Meta:
        verbose_name = u"Despesa direta por operação"
        verbose_name_plural = u"Despesas diretas por operação"

models.signals.post_save.connect(share_responsibility, sender=DirectExpense, dispatch_uid="directexpense")

class VariableExpense(Expense):
    start = models.DateField(u"De")
    end = models.DateField(u"Até")

    def share(self):
        self.share_by_flights()

    @property
    def flights(self):
        return Flight.objects.filter(date__gte=self.start, date__lte=self.end)
        
    def __unicode__(self):
        return '%s - %s' % (self.start.strftime('%d/%m/%Y'), self.end.strftime('%d/%m/%Y'))
    
    class Meta:
        verbose_name = u"Despesa variável operacional"
        verbose_name_plural = u"Despesas variáveis operacionais"

models.signals.post_save.connect(share_responsibility, sender=VariableExpense, dispatch_uid="variableexpense")

class FixedExpense(Expense):
    start = models.DateField(u"De")
    end = models.DateField(u"Até")
    
    repeat = models.IntegerField(u"Repetição", choices=((0, u"Não"),
                                                        (1, u"Mensalmente"),
                                                        (2, u"Anualmente"),
                                                        ), default=0)

    def __unicode__(self):
        return '%s - %s' % (self.start.strftime('%d/%m/%Y'), self.end.strftime('%d/%m/%Y'))
    
    def share(self):
        self.share_equally()
        
    class Meta:
        verbose_name = u"Despesa fixa operacional"
        verbose_name_plural = u"Despesas fixas operacionais"

models.signals.post_save.connect(share_responsibility, sender=FixedExpense, dispatch_uid="fixedexpense")

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

