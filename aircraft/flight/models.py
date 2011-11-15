# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


OPERATIONAL_BASE = 'SBJD'

OUTAGE_TYPES = (u'Mau uso',
                u'Fadiga',
                u'Eventual',
                u'Força maior',
                u'Desconhecido',
                )

OUTAGE_CHOICES = tuple([ (val, val) for val in OUTAGE_TYPES ])

def validate(sender, **kwargs):
    kwargs['instance'].validate()

class Person(models.Model):
    name = models.CharField(u"Nome", max_length=64)
    system_user = models.ForeignKey(User, verbose_name=u"usuário", blank=True, null=True)
    owner = models.BooleanField(u"É proprietário do avião?", default=False)
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u"Pessoa"

class FlightManager(models.Manager):
    @property
    def last(self):
        try:
            return self.all().order_by('-end_hobbs')[0]
        except IndexError:
            return None

class Flight(models.Model):
    number = models.IntegerField(u"#", editable=False)
    date = models.DateField(u"Data", blank=False, null=False)
    origin = models.CharField(u"Origem", max_length=4, blank=False, null=False)
    destiny = models.CharField(u"Destino", max_length=4, blank=False, null=False)
    start_hobbs = models.FloatField(u"Hobbs Saída", blank=False, null=False)
    end_hobbs = models.FloatField(u"Hobbs Chegada", blank=False, null=False)
    cycles = models.IntegerField(u"Ciclos", blank=False, null=False)
    mantainance = models.BooleanField(u"Traslado de manutenção?", blank=True, null=False, default=False)

    objects = FlightManager()

    def __init__(self, *args, **kwargs):
        super(Flight, self).__init__(*args, **kwargs)
        if not self.number:
            try:
                self.number = Flight.objects.last.number + 1
            except AttributeError:
                self.number = 1

    def validate(self):
        self.validate_hobbs()
        self.validate_date()

    def validate_hobbs(self):
        if not self.start_hobbs and self.number > 1:
            self.start_hobbs = Flight.objects.last.end_hobbs
        if self.number > 1 and abs(self.start_hobbs - Flight.objects.last.end_hobbs) > 1e-4:
            raise ValidationError(u"Hobbs inicial deste vôo deve ser igual ao final do último")
        if self.start_hobbs >= self.end_hobbs:
            raise ValidationError(u"Hobbs inicial deve ser menor que final")
        if self.start_hobbs < 0:
            raise ValidationError(u"Hobbs inicial deve ser maior que zero")
    def validate_date(self):
        if self.number > 1 and self.date < Flight.objects.last.date:
            raise ValidationError(u"Data do vôo deve ser posterior ao último vôo")

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
    
    def __unicode__(self):
        return '%04d %s %s %s %d-%d' % (self.number, self.date.strftime('%d/%m/%Y'), self.origin,
                                        self.destiny, self.start_hobbs, self.end_hobbs)

    class Meta:
        verbose_name = u"Vôo"
        ordering = ['-id']

models.signals.pre_save.connect(validate, sender=Flight, dispatch_uid="validate_flight")

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

class Outage(models.Model):
    flight = models.ForeignKey(Flight, null=True)
    outage_type = models.CharField(u"Tipo", max_length=16, choices=OUTAGE_CHOICES)
    discovery_date = models.DateField(u"Data de percepção da pane", blank=True, null=True)
    cause = models.CharField(u"Causa provável", max_length=255, blank=True, null=True)
    responsible = models.ForeignKey(Person, limit_choices_to={'owner': True},
                                    verbose_name = "Responsável", blank=True, null=True)

    def __unicode__(self):
        if self.flight:
            return '%s %s' % (self.flight, self.cause)
        else:
            return '%s %s' % (self.discovery_date.strftime('%d/%m/%Y'), self.cause)

    class Meta:
        verbose_name = u"Pane"

