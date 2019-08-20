from django import forms
from . import models



class DayFrequencyForm(forms.Form):
   days_choices = forms.ChoiceField(choices=models.DAYS)

class RateFrequencyForm(forms.Form):
   rate_choices = forms.ChoiceField(choices=models.RATE)