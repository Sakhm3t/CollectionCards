from django.test import TestCase, SimpleTestCase

from CollectionCards.views import *


class TestViews(SimpleTestCase):
    def test_index(self):
        """The index page loads properly"""
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_generation(self):
        response = self.client.get("/generate/", follow=True)
        self.assertEqual(response.status_code, 200)



class TestViewsWithDB(TestCase):

    @classmethod
    def setUp(cls):
        numbers_of_cards = 21
        for card in range(numbers_of_cards):
            BonusCard.objects.create(card_series="lo", sum_money=0, expiration_date='2022-05-01T00:00:00')

    def test_pagination_20(self):
        response = self.client.get(reverse('CollectionCards:full_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']) == 20, True)

    def test_view_shows_full_card_list(self):
        response = self.client.get("/full_list/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_shows_card_details(self):
        response = self.client.get("/detail_card/2/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_deletes_card(self):
        response = self.client.get("/detail_card/5/delete_card/", follow=True)
        self.assertEqual(response.status_code, 200)