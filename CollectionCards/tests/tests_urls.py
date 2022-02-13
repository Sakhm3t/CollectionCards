from django.test import SimpleTestCase
from django.urls import resolve
from CollectionCards.views import *


class TestURLs(SimpleTestCase):

    def test_generate_view(self):
        url = reverse('CollectionCards:generate')
        self.assertEquals(resolve(url).func, generation)

    def test_CardListView(self):
        url = reverse('CollectionCards:full_list')
        self.assertEquals(resolve(url).func.view_class, CardListView)

    def test_CardDetailView(self):
        url = reverse('CollectionCards:detail_card', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, CardDetailView)

    def test_CardUpdateView(self):
        url = reverse('CollectionCards:card_edit', kwargs={'pk': 2})
        self.assertEquals(resolve(url).func.view_class, CardUpdateView)

    def test_CardDeleteView(self):
        url = reverse('CollectionCards:Delete_card', kwargs={'pk': 3})
        self.assertEquals(resolve(url).func.view_class, CardDeleteView)

    def test_card_creation_view(self):
        url = reverse('CollectionCards:creation')
        self.assertEquals(resolve(url).func, card_creation)

    def test_searching_view(self):
        url = reverse('CollectionCards:list_for_search')
        self.assertEquals(resolve(url).func, searching)

    def test_search_result_view(self):
        url = reverse('CollectionCards:search_result')
        self.assertEquals(resolve(url).func, search_result)

    def test_actualize_db_view(self):
        url = reverse('CollectionCards:actualize')
        self.assertEquals(resolve(url).func, actualize_db)
