# -*- coding: utf-8 -*-

from counter import Counter
#from collections import Counter

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
    checked = models.BooleanField(u"Conferido", blank=True, default=False)
    calculated = models.BooleanField(u"Divisão OK", editable=False, default=True)

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
            
            calculated = False
            for owner, share in flight.responsibilities(ammount):
                calculated = True
                shares[owner.id] += share

            if not calculated:
                self.calculated = False
                self.save()
                return

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

        if not self.calculated:
            self.calculated = True
            self.save()

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
        if self.calculated:
            return ' / '.join([ 'R$ %.2f %s' % (r.ammount, r.owner.name) for r in self.responsibility_set.all() ])
        else:
            return u'NÃO CALCULADA'

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
    by = models.ForeignKey(Person,
                           verbose_name=u"De", related_name='transferences_made')
    to = models.ForeignKey(Person,
                           verbose_name=u"Para", related_name='transferences_received')
    ammount = models.FloatField(u"Valor", blank=False, null=False)
    paid = models.BooleanField(u"Pago", blank=True, default=True)

    triggered = False

    def __unicode__(self):
        return 'R$ %.2f %s - %s' % (self.ammount, unicode(self.by), unicode(self.to))

    class Meta:
        verbose_name = u"Interpagamento"
        ordering = ('paid', '-date')


def calculate_interpayments():

    creditors = []
    debtors = []

    total = 0

    for person in Person.objects.all():
        person.balance = 0
        person.balance += person.payment_set.filter(expense__calculated=True).aggregate(Sum('ammount'))['ammount__sum'] or 0
        person.balance -= person.responsibility_set.aggregate(Sum('ammount'))['ammount__sum'] or 0
        person.balance += person.transferences_made.filter(paid=True).aggregate(Sum('ammount'))['ammount__sum'] or 0
        person.balance -= person.transferences_received.filter(paid=True).aggregate(Sum('ammount'))['ammount__sum'] or 0
        
        if person.balance > 0:
            creditors.append(person)
        elif person.balance < 0:
            debtors.append(person)

        total += person.balance

    assert round(total, 2) == 0

    creditors = sorted(creditors, key=lambda p: -p.balance)
    debtors = sorted(debtors, key=lambda p: p.balance)

    result = []
    
    while creditors and debtors:
        ammount = min(abs(debtors[0].balance), creditors[0].balance)

        result.append((debtors[0], creditors[0], round(ammount, 2)))

        creditors[0].balance -= ammount
        debtors[0].balance += ammount

        if round(creditors[0].balance, 2) == 0:
            creditors.pop(0)
        if round(debtors[0].balance, 2) == 0:
            debtors.pop(0)

    return tuple(result)

def trigger_calculation(*args, **kwargs):
    Interpayment.triggered = True

def do_calculations(*args, **kwargs):
    if not Interpayment.triggered:
        return

    Interpayment.triggered = False
    for pay in Interpayment.objects.filter(paid=False):
        pay.delete()

    for pay in calculate_interpayments():
        Interpayment.objects.create(by=pay[0], to=pay[1], ammount=pay[2], paid=False)

    Interpayment.triggered = False
            
models.signals.post_save.connect(trigger_calculation, sender=Payment, dispatch_uid="interpayments_s1")
models.signals.post_save.connect(trigger_calculation, sender=Responsibility, dispatch_uid="interpayments_s2")
models.signals.post_save.connect(trigger_calculation, sender=Interpayment, dispatch_uid="interpayments_s3")
models.signals.post_delete.connect(trigger_calculation, sender=Payment, dispatch_uid="interpayments_d1")
models.signals.post_delete.connect(trigger_calculation, sender=Responsibility, dispatch_uid="interpayments_d2")
models.signals.post_delete.connect(trigger_calculation, sender=Interpayment, dispatch_uid="interpayments_d3")
