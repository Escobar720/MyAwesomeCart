from django.contrib import admin

# Register your models here.
from .models import product,Order,OrderUpdate,Contact
admin.site.register(product)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(OrderUpdate)