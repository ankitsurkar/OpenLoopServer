from django.contrib import admin
from .models import EndUser,PoS,RFID,Transaction,SpendingRules
# Register your models here.
admin.site.register(EndUser)
admin.site.register(PoS)
admin.site.register(RFID)
admin.site.register(Transaction)
admin.site.register(SpendingRules)
