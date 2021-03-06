from datetime import datetime
from django.db import models

# Create your models here.
from django.db.models import Q
from django.urls import reverse


class BonusCard(models.Model):
    """Class describes card details (database table)"""
    debit = 'db'
    loyalty = 'lo'
    credit = 'cr'
    TYPE_OF_CARD_CHOICES = [
        (debit, 'Debit'),
        (loyalty, 'Loyalty'),
        (credit, 'Credit'),
    ]
    card_series = models.CharField(max_length=2, choices=TYPE_OF_CARD_CHOICES, default=debit)
    card_number = models.BigAutoField(primary_key=True)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    date_of_use = models.DateTimeField(auto_now=True)
    sum_money = models.DecimalField(max_digits=10, decimal_places=2)
    card_status = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.card_number, self.card_series}"

    def get_absolute_url(self):
        return reverse('CollectionCards:detail_card', kwargs={'pk': self.pk})

    @staticmethod
    def actualize_database():
        count = BonusCard.objects.filter(~Q(card_status="expired")).filter(expiration_date__lte=datetime.now()).update(
            card_status="expired")
        return count


class PurchaseHistory(models.Model):
    """Class describes card purchase history"""
    bonus_card = models.ForeignKey('BonusCard', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.price}"
