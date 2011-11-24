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
    pilot = models.BooleanField(u"Pilota o avião?", default=False)
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
    date = models.DateField(u"Data")
    origin = models.CharField(u"Origem", max_length=4)
    destiny = models.CharField(u"Destino", max_length=4)
    pilot = models.ForeignKey(Person, verbose_name=u"Piloto", related_name="pilots",
                              limit_choices_to={'pilot': True}, null=True)
    copilot = models.ForeignKey(Person, verbose_name=u"Co-Piloto", related_name="copilots",
                                limit_choices_to={'pilot': True}, null=True, blank=True)
    takeoff_time = models.TimeField(u"Hora da decolagem", null=True)
    start_hobbs = models.FloatField(u"Hobbs Saída")
    end_hobbs = models.FloatField(u"Hobbs Chegada")
    cycles = models.IntegerField(u"Ciclos")
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
        self.start_hobbs = self.validate_hobbs(self.start_hobbs, self.end_hobbs)
        self.validate_date(self.date)
        self.origin = self.validate_origin(self.origin)

    def validate_hobbs(self, start_hobbs, end_hobbs):
        if not start_hobbs and self.number > 1:
            start_hobbs = Flight.objects.last.end_hobbs
        if self.number > 1 and abs(start_hobbs - self.previous_flight.end_hobbs) > 1e-4:
            raise ValidationError(u"Hobbs inicial deste vôo deve ser igual ao final do último (%.1f)" %
                                  self.previous_flight.end_hobbs
                                  )
        if start_hobbs >= end_hobbs:
            raise ValidationError(u"Hobbs inicial deve ser menor que final")
        if start_hobbs < 0:
            raise ValidationError(u"Hobbs inicial deve ser maior que zero")
        return start_hobbs

    def validate_date(self, date):
        if self.number > 1 and date < Flight.objects.last.date:
            raise ValidationError(u"Data do vôo deve ser posterior ao último vôo")
        return date
    def validate_origin(self, origin):
        if not origin and self.number > 1:
            origin = Flight.objects.last.destiny
        if self.number > 1 and origin != Flight.objects.last.destiny:
            raise ValidationError(u"Vôo deve partir do último local de destino")
        return origin

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
            if not pax_set:
                raise ValidationError(u'Não há PAX')

            total = pax_set.aggregate(Sum('ammount'))['ammount__sum']

            for pax in pax_set.all():
                yield pax.owner, ammount * float(pax.ammount) / total

    def _find_pax_set(self):
        if self.pax_set.count() > 0:
            return self.pax_set

        for flight in self.consecutive_flights():
            if flight.pax_set.count() > 0:
                return flight.pax_set
        return None

    def consecutive_flights(self):
        start = self.first_flight
        end = self.last_flight
        return Flight.objects.filter(number__gte=start.number,
                                     number__lte=end.number, 
                                     mantainance=False).order_by('number')
        
    @property
    def first_flight(self):
        if self.origin == OPERATIONAL_BASE:
            return self
        try:
            return Flight.objects.filter(number__lt=self.number, origin=OPERATIONAL_BASE).order_by('-number')[0]
        except IndexError:
            return self

    @property
    def last_flight(self):
        if self.destiny == OPERATIONAL_BASE:
            return self
        try:
            return Flight.objects.filter(number__gt=self.number, destiny=OPERATIONAL_BASE).order_by('number')[0]
        except IndexError:
            return self

    @property
    def previous_flight(self):
        if self.number == 1:
            return None
        return Flight.objects.get(number=self.number-1)
        
    @property
    def hobbs_desc(self):
        return '%d-%d' % (self.start_hobbs, self.end_hobbs)
    
    def __unicode__(self):
        return '#%04d %s %s %s %.1f-%.1f' % (self.number, self.date.strftime('%d/%m/%Y'), self.origin,
                                             self.destiny, self.start_hobbs, self.end_hobbs)

    class Meta:
        verbose_name = u"Vôo"
        ordering = ['-number']

models.signals.pre_save.connect(validate, sender=Flight, dispatch_uid="validate_flight")

class PAX(models.Model):
    flight = models.ForeignKey(Flight)
    owner = models.ForeignKey(Person, limit_choices_to={'owner': True})
    ammount = models.IntegerField()

    def propagate_changes(self):
        for flight in self.flight.consecutive_flights():
            for expense in flight.directexpense_set.all():
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

