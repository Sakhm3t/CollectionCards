from django import forms
from django.forms import ChoiceField

from .models import *


class GenerationForm(forms.Form):
    VALIDITY_CHOICES = [
        ('30', '1 month'),
        ('182', '6 months'),
        ('365', '1 year'),
    ]
    SERIES_CHOICES = [
        ('db', 'Debit'),
        ('lo', 'Loyalty'),
        ('cr', 'Credit'),
    ]
    number_of_cards = forms.IntegerField(min_value=1, max_value=1000)
    series_of_cards = forms.ChoiceField(choices=SERIES_CHOICES, )
    validity = forms.ChoiceField(choices=VALIDITY_CHOICES)


class UpdateCardForm(forms.ModelForm):
    class Meta:
        model = BonusCard
        fields = ['card_status']
        widgets = {'card_status': forms.RadioSelect()}


class DeleteCardForm(forms.ModelForm):
    class Meta:
        model = BonusCard
        fields = ['card_number']


class SearchingForm(forms.Form):
    STATUS_CHOICES = [
        ('', '- Empty -'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    SERIES_CHOICES = [
        ('', '- Empty -'),
        ('db', 'Debit'),
        ('lo', 'Loyalty'),
        ('cr', 'Credit'),
    ]
    card_number = forms.CharField(required=False)
    card_series = forms.ChoiceField(choices=SERIES_CHOICES, required=False)
    date_of_issue = forms.DateTimeField(required=False)
    expiration_date = forms.DateTimeField(required=False)
    date_of_use = forms.DateTimeField(required=False)
    sum_money = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    card_status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
