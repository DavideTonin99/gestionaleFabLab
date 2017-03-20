from django.contrib import admin

from .models import Person, Event, Subscription, Processing

# Register your models here.

admin.site.register(Person)
admin.site.register(Event)
admin.site.register(Subscription)
admin.site.register(Processing)
