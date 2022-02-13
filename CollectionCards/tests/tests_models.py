from django.test import TestCase
from CollectionCards.models import *


class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        BonusCard.objects.create(card_series="db", sum_money=1000.32, expiration_date='2004-05-23T14:25:10')
        BonusCard.objects.create(card_series="lo", sum_money=10.00, expiration_date='2022-05-01T00:00:00')
        PurchaseHistory.objects.create(price=100.12, bonus_card_id=1)
        PurchaseHistory.objects.create(price=70.00, bonus_card_id=2)

    def test_get_absolute_url(self):
        test = BonusCard.objects.get(pk=2)
        self.assertEquals(test.get_absolute_url(), '/detail_card/2/')

    def test_str(self):
        test = BonusCard.objects.get(pk=1)
        self.assertEquals(str(test), "(1, 'db')")

    def test_actualize_database(self):
        self.assertEquals(BonusCard.actualize_database(), 1)

    def test_str_pur(self):
        test = PurchaseHistory.objects.get(pk=1)
        self.assertEquals(str(test), "100.12")
