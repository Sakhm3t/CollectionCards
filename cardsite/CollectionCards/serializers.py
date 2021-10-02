from rest_framework.serializers import ModelSerializer

from .models import BonusCard


class BonusCardSerializer(ModelSerializer):
    class Meta:
        model = BonusCard
        fields = ["card_number", "card_series", "date_of_issue", "expiration_date", "card_status"]
