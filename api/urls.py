from django.urls import path

from . import v1

urlpatterns = [
    path('v1/', v1.views.index, name='index'),
    path('v1/scooters/', v1.scooters.views.index, name='index'),
    path('v1/scooters/available/', v1.scooters.views.available, name='available'),
    # The below are POST requests and can't have the trailing slash (APPEND_SLASH=True)
    path('v1/scooters/reserve', v1.scooters.views.reserve, name='reserve'),
    path('v1/scooters/end_reservation', v1.scooters.views.end_reservation, name='end_reservation'),
    path('v1/scooters/calc_payment/<int:scooter_id>', v1.scooters.views.calc_payment, name='calc_payment'),
    path('v1/scooters/pay/<int:payment_id>', v1.scooters.views.pay, name='pay'),
]
