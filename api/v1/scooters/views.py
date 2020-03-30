import json

from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse,
    JsonResponse,
)

from .exceptions import InvalidParamError
from .models import (
    Scooter,
    Payments,
)
from.serializers import (
    serialize_scooter,
    serialize_available_scooters,
)
from .validators import validate_param


def index(request):
    # Probably a list of all scooters and their reservation status
    return HttpResponse("scooters index")


def available(request):
    if request.method == 'GET':
        try:
            latitude = validate_param('lat', request.GET.get('lat', '0'))
            longitude = validate_param('lng', request.GET.get('lng', '0'))
            radius = validate_param('radius', request.GET.get('radius', '0'))
        except InvalidParamError as e:
            data = {'error': e.error}
            return JsonResponse(data, status=e.status_code)

        scooters = Scooter.get_available_scooters_by_radius(
            latitude,
            longitude,
            radius
        )

        return JsonResponse(serialize_available_scooters(scooters), safe=False)
    else:
        data = {'error': 'method not supported'}
        return JsonResponse(data, status=405)


@csrf_exempt
def reserve(request):
    if request.method == 'POST':
        scooter_id = request.GET.get('id')
        try:
            scooter_id = int(scooter_id)
        except (ValueError, TypeError):
            data = {'error': 'id must be an int'}
            return JsonResponse(data, status=422)

        scooter = Scooter.get_scooter_by_id(scooter_id)
        if scooter and not scooter.is_reserved:
            scooter.reserve()
            return JsonResponse(serialize_scooter(scooter), safe=False)
        else:
            data = {'error': 'Scooter not found or unavailable'}
            return JsonResponse(data, status=404)
    else:
        data = {'error': 'method not supported'}
        return JsonResponse(data, status=405)


@csrf_exempt
def end_reservation(request):
    if request.method == 'POST':
        scooter_id = request.GET.get('id')
        try:
            scooter_id = int(scooter_id)
        except (ValueError, TypeError):
            data = {'error': 'id must be an int'}
            return JsonResponse(data, status=422)

        scooter = Scooter.get_scooter_by_id(scooter_id)
        if scooter and scooter.is_reserved:
            scooter.end_reservation()
            return JsonResponse(serialize_scooter(scooter), safe=False)
        else:
            data = {'error': 'Scooter not found or not reserved'}
            return JsonResponse(data, status=404)
    else:
        data = {'error': 'method not supported'}
        return JsonResponse(data, status=405)


@csrf_exempt
def calc_payment(request, scooter_id):
    if request.method == 'POST':
        try:
            params = json.loads(request.body)
        except:
            data = {'error': 'Invalid request body'}
            return JsonResponse(data, status=422)
        try:
            distance_traveled = validate_param('distance_traveled',
                                               params.get('distance_traveled'))
            payment_rate = validate_param('payment_rate', params.get('payment_rate'))
        except InvalidParamError as e:

            data = {'error': e.error}
            return JsonResponse(data, status=e.status_code)
        scooter = Scooter.get_scooter_by_id(scooter_id)
        if not scooter:
            data = {'error': 'Scooter not found'}
            return JsonResponse(data, status=404)

        payment = Payments.create(
            scooter=scooter,
            distance_traveled=distance_traveled,
            payment_rate=payment_rate,
        )

        data = {
            'id': payment.pk,
            'payment_due': payment.get_payment_amount()
        }
        return JsonResponse(data)
    else:
        data = {'error': 'method not supported'}
        return JsonResponse(data, status=405)


@csrf_exempt
def pay(request, payment_id):
    if request.method == 'POST':
        payment = Payments.get_payment_by_id(payment_id)
        if not payment:
            data = {'error': 'Payment not found'}
            return JsonResponse(data, status=404)

        payment.pay()

        data = {
            'id': payment.pk,
            'is_paid': payment.is_paid
        }
        return JsonResponse(data)
    else:
        data = {'error': 'method not supported'}
        return JsonResponse(data, status=405)
