from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(EndUser)
admin.site.register(Vendor)
admin.site.register(PoS)
admin.site.register(RFID)
admin.site.register(Transaction)
