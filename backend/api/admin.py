from django.contrib import admin

from .models import Part, PartCompatibility, Order, OrderItem

admin.site.register(Part)
admin.site.register(PartCompatibility)
admin.site.register(Order)
admin.site.register(OrderItem)
