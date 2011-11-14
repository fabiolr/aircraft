# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum

from flight.models import Person
from expense.models import Payment, Responsibility

class Interpayment(models.Model):
    date = models.DateField(u"Data", null=True)
    by = models.ForeignKey(Person, limit_choices_to={'owner': True},
                           verbose_name=u"De", related_name='transferences_made')
    to = models.ForeignKey(Person, limit_choices_to={'owner': True},
                           verbose_name=u"Para", related_name='transferences_received')
    ammount = models.FloatField(u"Valor", blank=False, null=False)
    paid = models.BooleanField(u"Pago", blank=True, default=True)

    def __unicode__(self):
        return 'R$ %.2f %s - %s' % (self.ammount, self.by, self.to)

    class Meta:
        verbose_name = u"Interpagamento"
        ordering = ('paid', '-date')


def calculate_interpayments():

    creditors = []
    debtors = []

    total = 0

    for p in Person.objects.all():
        p.balance = 0
        p.balance += p.payment_set.aggregate(Sum('ammount'))['ammount__sum'] or 0
        p.balance -= p.responsibility_set.aggregate(Sum('ammount'))['ammount__sum'] or 0
        p.balance += p.transferences_made.filter(paid=True).aggregate(Sum('ammount'))['ammount__sum'] or 0
        p.balance -= p.transferences_received.filter(paid=True).aggregate(Sum('ammount'))['ammount__sum'] or 0
        
        if p.balance > 0:
            creditors.append(p)
        elif p.balance < 0:
            debtors.append(p)

        total += p.balance

    assert total == 0
    
    creditors = sorted(creditors, key=lambda p: p.balance)
    debtors = sorted(debtors, key=lambda p: -p.balance)

    result = []
    
    while creditors and debtors:
        ammount = min(abs(debtors[0].balance), creditors[0].balance)

        result.append((debtors[0], creditors[0], ammount))

        creditors[0].balance -= ammount
        debtors[0].balance += ammount

        if round(creditors[0].balance) == 0:
            creditors.pop(0)
        if round(debtors[0].balance) == 0:
            debtors.pop(0)

    return tuple(result)

calculation = { 'triggered': True }

def trigger_calculation(*args, **kwargs):
    calculation['triggered'] = True

def do_calculations(*args, **kwargs):
    if not calculation['triggered']:
        return

    calculation['triggered'] = False
    for pay in Interpayment.objects.filter(paid=False):
        pay.delete()

    for pay in calculate_interpayments():
        Interpayment.objects.create(by=pay[0], to=pay[1], ammount=pay[2], paid=False)
            
models.signals.post_save.connect(trigger_calculation, sender=Payment, dispatch_uid="interpayments_1")
models.signals.post_save.connect(trigger_calculation, sender=Responsibility, dispatch_uid="interpayments_2")
models.signals.post_save.connect(trigger_calculation, sender=Interpayment, dispatch_uid="interpayments_3")
