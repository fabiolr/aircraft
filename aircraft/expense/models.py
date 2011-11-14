# -*- coding: utf-8 -*-

import collections

from django import core
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

from flight.models import Person, Flight

EXPENSE_TYPES = {1: u'Direta por operação',
                 2: u'Variável operacional',
                 3: u'Fixa operacional',
                 4: u'Pane',
                 }

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
        self.apply_share(((owner, self.ammount),))
            
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

