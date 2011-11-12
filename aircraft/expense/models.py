# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from signals import calculate_expense_responsibility

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

    def __unicode__(self):
        return ' '.join((self.date, self.origin, self.destiny))

    class Meta:
        verbose_name = u"Vôo"

class PAX(models.Model):
    flight = models.ForeignKey(Flight)
    owner = models.ForeignKey(Person, limit_choices_to={'owner': True})
    ammount = models.IntegerField()

    def __unicode__(self):
        return '%s %.2f' % (self.owner.name, self.ammount)
    
    class Meta:
        verbose_name = u"PAX"
        verbose_name_plural = u"PAX"
    
class ExpenseCategory(models.Model):
    name = models.CharField(u"Nome", max_length=32)
    expense_type = models.IntegerField(u"Tipo de despesa", choices=EXPENSE_TYPES.items())

    def __unicode__(self):
        return '%s - %s' % (EXPENSE_TYPES[self.expense_type], self.name)
    
    class Meta:
        verbose_name = u"Categoria de despesas"
        verbose_name_plural = u"Categorias de despesas"
        ordering = ('expense_type', 'name')
    
class Expense(models.Model):
    ammount = models.FloatField(u"Valor", blank=False, null=False)
    date = models.DateField(u"Data", blank=False, null=False)
    category = models.ForeignKey(ExpenseCategory, blank=True, null=True)

    def __unicode__(self):
        return '%s %.2f' % (self.date, self.ammount)

    def __repr__(self):
        return '%s %.2f' % (self.__class__.__name__, self.ammount)

    class Meta:
        verbose_name = u"Despesa"
        ordering = ['-date']

models.signals.post_save.connect(calculate_expense_responsibility, sender=Expense)

class Payment(models.Model):
    expense = models.ForeignKey(Expense)
    person = models.ForeignKey(Person)
    ammount = models.FloatField()

    def __unicode__(self):
        return '%s %.2f' % (self.person.name, self.ammount)
    
    class Meta:
        verbose_name = u"Pagamento"

class Responsibility(models.Model):
    expense = models.ForeignKey(Expense)
    owner = models.ForeignKey(Person, limit_choices_to={'owner': True})
    ammount = models.FloatField()

    def __unicode__(self):
        return '%s %.2f' % (self.owner.name, self.ammount)
    
    class Meta:
        verbose_name = u"Responsabilidade"

class DirectExpense(Expense):
    flight = models.ForeignKey(Flight) 
    description = models.CharField(u"Descrição", max_length=255)

    class Meta:
        verbose_name = u"Despesa direta por operação"
        verbose_name_plural = u"Despesas diretas por operação"

class VariableExpense(Expense):
    start = models.DateField(u"De")
    end = models.DateField(u"Até")
    
    class Meta:
        verbose_name = u"Despesa variável operacional"
        verbose_name_plural = u"Despesas variáveis operacionais"


class FixedExpense(Expense):
    start = models.DateField(u"De")
    end = models.DateField(u"Até")
    
    repeat = models.IntegerField(u"Repetição", choices=((0, u"Não"),
                                                        (1, u"Mensalmente"),
                                                        (2, u"Anualmente"),
                                                        ))
    class Meta:
        verbose_name = u"Despesa fixa operacional"
        verbose_name_plural = u"Despesas fixas operacionais"


class HourlyMantainance(Expense):
    mantainance_date = models.DateField(u"Data de chegada na oficina")
    hobbs = models.FloatField(u"Hobbs de chegada na oficina")
    hours = models.IntegerField(u"Nº de horas da inspeção")
    obs = models.CharField(u"Observações", max_length=255)

    class Meta:
        verbose_name = u"Manutenção por hora"
        verbose_name_plural = u"Manutenções por hora"
        

class ScheduleMantainance(Expense):
    entrance_date = models.DateField(u"Data de chegada na oficina")
    period = models.IntegerField(u"Período vencido em dias")

    class Meta:
        verbose_name = u"Manutenção calendárica"
        verbose_name_plural = u"Manutenções calendáricas"
    

class EventualMantainance(Expense):
    flight = models.ForeignKey(Flight, blank=True)
    outage_type = models.CharField(u"Tipo", max_length=16, choices=OUTAGE_CHOICES)
    discovery_date = models.DateField(u"Data de percepção da pane")
    cause = models.CharField(u"Causa provável", max_length=255)
    responsible = models.ForeignKey(Person, limit_choices_to={'owner': True},
                                    verbose_name = "Responsável")

    class Meta:
        verbose_name = u"Manutenção eventual"
        verbose_name_plural = u"Manuenções eventuais (Panes)"

class Payment(models.Model):
    date = models.DateField(u"Data")
    by = models.ForeignKey(Person, limit_choices_to={'owner': True},
                           verbose_name=u"De", related_name='payments_made')
    to = models.ForeignKey(Person, limit_choices_to={'owner': True},
                           verbose_name=u"Para", related_name='payments_received')
    ammount = models.FloatField(u"Valor", blank=False, null=False)


