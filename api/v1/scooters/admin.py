from django.contrib import admin

from .models import (
    Scooter,
    Payments,
)


class ScooterAdmin(admin.ModelAdmin):
    pass
admin.site.register(Scooter, ScooterAdmin)


class PaymentsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payments, PaymentsAdmin)

