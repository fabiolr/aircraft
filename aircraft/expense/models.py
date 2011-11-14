# -*- coding: utf-8 -*-

import collections
from datetime import timedelta

from django import core
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from signals import calculate_expense_responsibility

OPERATIONAL_BASE = 'SBJD'

EXPENSE_TYPES = {1: u'Direta por operação',
                 2: u'Variável operacional',
                 3: u'Fixa operacional',
                 }

OUTAGE_TYPES = (u'Mau uso',
                u'Fadiga',
                u'Eventual',
                u'Força maior',
                u'Desconhecido',
                )

OUTAGE_CHOICES = tuple([ (val, val) for val in OUTAGE_TYPES ])

class Person(models.Model):
    name = models.CharField(u"Nome", max_length=64)
    system_user = models.ForeignKey(User, verbose_name=u"usuário", blank=True, null=True)
    owner = models.BooleanField(u"É proprietário do avião?", default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u"Pessoa"
    
class Flight(models.Model):
    date = models.DateField(u"Data", blank=False, null=False)
    origin = models.CharField(u"Origem", max_length=4, blank=False, null=False)
    destiny = models.CharField(u"Destino", max_length=4, blank=False, null=False)
    start_hobbs = models.FloatField(u"Hobbs Saída", blank=False, null=False)
    end_hobbs = models.FloatField(u"Hobbs Chegada", blank=False, null=False)
    cycles = models.IntegerField(u"Ciclos", blank=False, null=False)
    mantainance = models.BooleanField(u"Traslado de manutenção?", blank=True, null=False, default=False)

    @property
    def hobbs(self):
        return self.end_hobbs - self.start_hobbs

    def responsibilities(self, ammount=1.0):
        if self.mantainance:
            owners = Person.objects.filter(owner=True)
            for owner in owners.all():
                yield owner, ammount/owners.count()

        else:
            pax_set = self._find_pax_set()
            total = pax_set.aggregate(Sum('ammount'))['ammount__sum']

            for pax in pax_set.all():
                yield pax.owner, ammount * float(pax.ammount) / total

    def _find_pax_set(self):
        if self.pax_set.count() > 0:
            return self.pax_set

        if self.origin == OPERATIONAL_BASE:
            raise ValidationError("Não há nenhum PAX")

        try:
            last = Flight.objects.filter(start_hobbs__lt = self.start_hobbs).order_by('-start_hobbs')[0]
        except IndexError:
            raise ValidationError("Não há nenhum PAX")

        return last._find_pax_set()

    @property
    def hobbs_desc(self):
        return '%d-%d' % (self.start_hobbs, self.end_hobbs)
    
    @property
    def number(self):
        return '#%04d' % self.id

    def __unicode__(self):
        return '%s %s %s %s %d-%d' % (self.number, self.date.strftime('%d/%m/%Y'), self.origin,
                                      self.destiny, self.start_hobbs, self.end_hobbs)

    class Meta:
        verbose_name = u"Vôo"
        ordering = ['-id']

class PAX(models.Model):
    flight = models.ForeignKey(Flight)
    owner = models.ForeignKey(Person, limit_choices_to={'owner': True})
    ammount = models.IntegerField()

    def propagate_changes(self):
        for expense in self.flight.directexpense_set.all():
            expense.save()

    def __unicode__(self):
        return '%s %.2f' % (self.owner.name, self.ammount)
    
    class Meta:
        verbose_name = u"PAX"
        verbose_name_plural = u"PAX"
    
def propagate_pax_changes(sender, **kwargs):
    kwargs['instance'].propagate_changes()
    
models.signals.post_save.connect(propagate_pax_changes, sender=PAX, dispatch_uid="pax")

class ExpenseCategory(models.Model):
    name = models.CharField(u"Nome", max_length=32)
    expense_type = models.IntegerField(u"Tipo de despesa", choices=EXPENSE_TYPES.items())

    def __unicode__(self):
        return '%s' % self.name
    
    class Meta:
        verbose_name = u"Categoria de despesas"
        verbose_name_plural = u"Categorias de despesas"
        ordering = ('expense_type', 'name')
    
class Expense(models.Model):
    date = models.DateField(u"Data do pagamento", blank=False, null=False)
    category = models.ForeignKey(ExpenseCategory, verbose_name=u'Categoria', blank=True, null=True)

    @property
    def ammount(self):
        return self.payment_set.aggregate(Sum('ammount'))['ammount__sum']
    
    def share_by_flights(self):
        if self.flights.count() == 0:
            return self.share_equally()
        
        total_hobbs =  self.flights.aggregate(Sum('end_hobbs'))['end_hobbs__sum']
        total_hobbs -= self.flights.aggregate(Sum('start_hobbs'))['start_hobbs__sum']
        
        shares = collections.Counter()

        for flight in self.flights:
            ammount = self.ammount * flight.hobbs / total_hobbs
            
            for owner, share in flight.responsibilities(ammount):
                shares[owner.id] += share

        shares = [ (Person.objects.get(id=item[0]), item[1]) for item in shares.items() ]
        
        return self.apply_share(shares)

    def share_equally(self):
        owners = Person.objects.filter(owner=True)
        shares = [ (owner, self.ammount/owners.count()) for owner in owners.all() ]
        return self.apply_share(shares)        

    def blame(self, owner):
        self.apply_share(((self.responsible, self.ammount),))
            
    def apply_share(self, responsibilities):
        for resp in self.responsibility_set.all():
            resp.delete()

        for owner, responsibility in responsibilities:
            self.responsibility_set.create(ammount=responsibility, owner=owner)

    def child(self):
        if self.__class__ is not Expense:
            return self
        for attr in ('directexpense', 'variableexpense', 'fixedexpense',
                     'hourlymantainance', 'schedulemantainance', 'eventualmantainance'):
            try:
                return getattr(self, attr)
            except Expense.DoesNotExist:
                pass

    child.short_description = u'Despesa'

    @property
    def responsibility(self):
        return ' / '.join([ 'R$ %.2f %s' % (r.ammount, r.owner.name) for r in self.responsibility_set.all() ])

    def __unicode__(self):
        return '%s %.2f' % (self.__class__._meta.verbose_name, self.ammount)

    def __repr__(self):
        return '%s %.2f' % (self.__class__.__name__, self.ammount)

    class Meta:
        verbose_name = u"Despesa"
        ordering = ['-date']

class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    paid_by = models.ForeignKey(Person, verbose_name=u"Pessoa")
    ammount = models.FloatField(u"Valor pago")

    def __unicode__(self):
        return '%s %.2f' % (self.paid_by.name, self.ammount)
    
    class Meta:
        verbose_name = u"Pagamento"
        verbose_name_plural = u"Pago por"

def share_expense_responsibility(sender, **kwargs):
    try:
        kwargs['instance'].expense.child().share()
    except AttributeError:
        # tests
        pass
    
models.signals.post_save.connect(share_expense_responsibility, sender=Payment, dispatch_uid="payment")

class Responsibility(models.Model):
    expense = models.ForeignKey(Expense)
    owner = models.ForeignKey(Person, limit_choices_to={'owner': True})
    ammount = models.FloatField()

    def __unicode__(self):
        return '%s %.2f' % (self.owner.name, self.ammount)
    
    class Meta:
        verbose_name = u"Responsabilidade"
        ordering = [u"owner__name"]

#signal
def share_responsibility(sender, **kwargs):
    if kwargs['instance'].ammount:
        kwargs['instance'].share()

class DirectExpense(Expense):
    flight = models.ForeignKey(Flight, verbose_name=u"Vôo") 
    description = models.CharField(u"Descrição", max_length=255)

    def share(self):
        self.apply_share(self.flight.responsibilities(self.ammount))

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
    flight = models.ForeignKey(Flight, null=True)
    outage_type = models.CharField(u"Tipo", max_length=16, choices=OUTAGE_CHOICES)
    discovery_date = models.DateField(u"Data de percepção da pane", blank=True, null=True)
    cause = models.CharField(u"Causa provável", max_length=255, blank=True, null=True)
    responsible = models.ForeignKey(Person, limit_choices_to={'owner': True},
                                    verbose_name = "Responsável", blank=True, null=True)

    def share(self):
        if self.responsible:
            self.blame(self.responsible)
        else:
            self.share_equally()

    def __unicode__(self):
        if self.flight:
            return '%s %s' % (self.flight, self.cause)
        else:
            return '%s %s' % (self.discovery_date.strftime('%d/%m/%Y'), self.cause)

    class Meta:
        verbose_name = u"Manutenção eventual"
        verbose_name_plural = u"Manuenções eventuais (Panes)"

models.signals.post_save.connect(share_responsibility, sender=EventualMantainance, dispatch_uid="emantainance")

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
            
models.signals.post_save.connect(trigger_calculation, sender=FixedExpense, dispatch_uid="interpayments_1")
models.signals.post_save.connect(trigger_calculation, sender=Interpayment, dispatch_uid="interpayments_3")


#core.signals.request_finished.connect(do_calculations, sender=core.handler.base.BaseHandler,
#                                      dispatch_uid="do_calc")
