from django.contrib import admin

from .models import Customer, Event, Subscription, Processing

admin.site.register(Customer)
admin.site.register(Event)
admin.site.register(Subscription)
admin.site.register(Processing)
