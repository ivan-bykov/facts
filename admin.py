from django.contrib import admin
from facts.models import Fact, Item, Exchange

# Register your models here.
admin.site.register(Fact)
admin.site.register(Item)
admin.site.register(Exchange)
