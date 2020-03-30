def serialize_scooter(scooter):
    return {
        'id': scooter.pk,
        'lat': scooter.latitude,
        'lng': scooter.longitude,
    }

def serialize_available_scooters(scooters):
    return [serialize_scooter(scooter) for scooter in scooters]
