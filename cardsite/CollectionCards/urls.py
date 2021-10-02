from django.urls import path

from .views import *

app_name = 'CollectionCards'
urlpatterns = [
    path('', task),
    path('generate/', generation, name='generate'),
    path('full_list/', CardListView.as_view(), name='full_list'),
    path('detail_card/<int:pk>/', CardDetailView.as_view(), name='detail_card'),
    path('detail_card/<int:pk>/edit_card/', CardUpdateView.as_view(), name='card_edit'),
    path('detail_card/<int:pk>/delete_card/', CardDeleteView.as_view(), name='Delete_card'),
    path('process/', card_creation),
    path('searching/', searching, name='list_for_search'),
    path('result/', search_result, name='search_result'),
    path('actualize/', actualize_db, name='actualize'),
    path('api/', expired_card_api_view)
]
