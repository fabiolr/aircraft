# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from models import Flight, PAX

class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight

    def __init__(self, *argz, **kwargs):
        last = Flight.objects.last
        if not kwargs.get('instance') and last:
            kwargs['initial'] = { 'date': date.today(),
                                  'origin': last.destiny,
                                  'start_hobbs': last.end_hobbs,
                                  }

        super(FlightForm, self).__init__(*argz, **kwargs)

    def clean(self):
        self.cleaned_data['start_hobbs'] = self.instance.validate_hobbs(self.cleaned_data.get('start_hobbs'),
                                                                        self.cleaned_data.get('end_hobbs'))
        return self.cleaned_data

    def clean_date(self):
        return self.instance.validate_date(self.cleaned_data.get('date'))

    def clean_origin(self):
        return self.instance.validate_origin(self.cleaned_data.get('origin'))

class PAXForm(forms.ModelForm):

    class Meta:
        model = PAX

    def clean_ammount(self):
        if self.cleaned_data['ammount'] < 1:
            raise ValidationError("A quantidade de pessoas deve ser maior que zero")
        return self.cleaned_data['ammount']
    


        
