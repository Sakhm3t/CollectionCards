from django.contrib import admin

# Register your models here.
from .models import BonusCard, PurchaseHistory

admin.site.register(BonusCard)
admin.site.register(PurchaseHistory)