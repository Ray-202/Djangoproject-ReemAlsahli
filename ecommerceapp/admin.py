from django.contrib import admin
from .models import Storetype, items, itemsdetails, Coffee
# Register your models here.
admin.site.register(Storetype)
admin.site.register(items)
admin.site.register(itemsdetails)
admin.site.register(Coffee)