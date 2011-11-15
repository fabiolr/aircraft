# -*- coding: utf-8 -*-

#from counter import Counter
from collections import Counter

from django.db import models
from django.db.models import Sum

from flight.models import Person

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
        
        shares = Counter()

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
        verbose_name_plural = u"Todas as despesas"
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
