from django.db import models
from django.utils import timezone


class Scooter(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # ideally use a spatial db and geodjango
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_reserved = models.BooleanField(default=False)

    def __repr__(self):
        return '<{}, {}>'.format(self.latitude, self.longitude)

    def __str__(self):
        return '<{}, {}>'.format(self.latitude, self.longitude)

    @classmethod
    def get_available_scooters_by_radius(cls, latitude, longitude, radius):
        min_latitude = min(latitude - radius/2, latitude + radius/2)
        max_latitude = max(latitude - radius/2, latitude + radius/2)
        min_longitude = min(longitude - radius/2, longitude + radius/2)
        max_longitude = max(longitude - radius/2, longitude + radius/2)

        return cls.objects.filter(
            latitude__lte=max_latitude,
            latitude__gte=min_latitude,
            longitude__lte=max_longitude,
            longitude__gte=min_longitude,
            is_reserved=False,
        ).all()

    @classmethod
    def get_scooter_by_id(cls, scooter_id):
        return cls.objects.filter(pk=scooter_id).first()

    def reserve(self):
        self.is_reserved = True
        self.save()

    def end_reservation(self):
        self.is_reserved = False
        self.save()


class Payments(models.Model):
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    distance_traveled = models.DecimalField(max_digits=9, decimal_places=6)
    payment_rate = models.DecimalField(max_digits=9, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    refund_date = models.DateTimeField(default=None, null=True, blank=True)

    @classmethod
    def create(cls, scooter, distance_traveled, payment_rate):
        payment = cls(
            scooter=scooter,
            distance_traveled=distance_traveled,
            payment_rate=payment_rate,
        )
        payment.save()
        return payment

    @classmethod
    def get_payment_by_id(cls, payment_id):
        return cls.objects.filter(pk=payment_id).first()

    def get_payment_amount(self):
        return round(float(self.distance_traveled * self.payment_rate), 2)

    def pay(self):
        self.is_paid = True
        self.save()

    def refund(self):
        self.is_paid = False
        self.refund_date = timezone.now()
        self.save()
