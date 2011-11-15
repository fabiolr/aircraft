# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from models import Flight

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

