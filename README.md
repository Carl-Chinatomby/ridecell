# Ridecell scooter interview problem

## Problem description
<code>
    Problem Overview

    Each scooter has a unique id, and its current location (lat, lng). Users should be able to view scooters, start a scooter reservation, end their reservation, and pay for the distance they traveled. Build REST APIs for the following and share the Git repository with us. You can populate your database with any dummy data you want. You can write the code in Python/Django, Ruby/Rails, JS/Express or another web framework, but we have a preference for Python/Django.

    Requirements

    Search for an address and find nearby available scooters. (input: lat, lng, radius in meters. Output - list of parking spots within the radius).
    Reserve a scooter.
    Bonus

    Automated tests
    Ending reservations
    Any kind of mock payments
    Proposals on how to improve the APIs
    Sample API requests/Responses:

    1.) GET /api/v1/scooters/available?lat=37.788989&lng=-122.404810&radius=20.0

    Response:

    [
        {
            "id": 10,
            "lat": 37.788548,
            "lng": -122.411548
        },
        {
            "id": 8,
            "lat": 37.783223,
            "lng": -122.398630
        }
    ]

    2.) POST /api/v1/scooters/reserve?id=10

    Once you reserve scooter 10, if you call the scooters available api (first example endpoint), it should not return scooter 10 as it is reserved.

</code>

## Installation

This project is dockerized. You can install docker by following the instructions on their [official website.](https://www.docker.com/get-started)

Once that is done you can setup the set up the project by typing in <code>docker-compose up</code> in a terminal. This will download/build all images, install any packages, run any migrations, and preload the db. After the first time these operations become no-ops unless migrations have changed.

You can always do <code>docker-compose down</code> to stop all containers. Other
useful commands can be found by executing <code>docker-compose help</code> or reading
the official documentation.

## Running the app
The app can be run by executing <code>docker-compose up</code> in the terminal.
The base url for all endpoints is [http://0.0.0.0:8000/api/v1/scooters/](http://0.0.0.0:8000/api/v1/scooters/)

## Running the tests
Ideally there would be a test container and test_requirements. Since this is a simple project, and I didn't want to scope, I ran the tests inside the container. You can do so by following these instructions in a terminal:
1. docker exec -it ridecell_web bash
1. /opt/venv/bin/python scooters/manage.py test

You can also run other django commands from here for debugging purposes or manual changes.

## Endpoints

### /api/v1/scooters/available

Parameters:
* lat (decimal) - the latitude for the radius
* lng (decimal) - the longitude for the radius
* radius (decimal) - radius to check for available scooters

Request:

**GET /api/v1/scooters/available?lat=37.788989&lng=-122.404810&radius=20.0**

Response:

    [
        {
            "id": 10,
            "lat": 37.788548,
            "lng": -122.411548
        },
        {
            "id": 8,
            "lat": 37.783223,
            "lng": -122.398630
        }
    ]

### /api/v1/scooters/reserve

Parameters:
* id (int) - the id of the scooter to be reserved

Request:

**POST /api/v1/scooters/reserve?id=10**

Response:

    {
      "id": 1,
      "lat": "37.788548",
      "lng": "-122.411548"
    }

### /api/v1/scooters/end_reservation

Parameters:
* id (int) - the id of the scooter to end reservation on

Request:

**POST /api/v1/scooters/end_reservation?id=10**

Response:

    {
      "id": 1,
      "lat": "37.788548",
      "lng": "-122.411548"
    }

### /api/v1/scooters/calc_payment/<scooter_id>

Parameters:
* distance_traveled (decimal) - the number of meters traveled
* payment_rate (float) - The rate per meter

Request (Note: Parameters are passed as POSTDATA and not url parameters):

**POST /api/v1/scooters/calc_payment/<scooter_id>**

Response:

    {
      "id": 1,
      "payment_due": 50.0
    }

### /api/v1/scooters/pay/<payment_id>

Request (Note: payment_id is obtained from response of calc_payment):

**POST /api/v1/scooters/calc_payment/<payment_id>**

Response:

    {
    	'id': 2,
    	'is_paid': True
    }

-----

## Potential API improvements

* The API is missing a user model authentication/authorization system. While out of the scope of this project, it would be necessary for any production API that deals with reservations and payments. ALL the POST APIs would require it.
* For all the POST API's we should not be passing in URL parameters. THE URLs should reflect the id of the object being modified and any additional data needed should be sent via the body of the request. I have created an example of this in <code>/calc_payment</code> and <code>/pay</code> example endpoints.
* I would enable caching on the <code>/available</code> endpoint where the cache is dirtied whenever someone reserves a scooter.
* We would ideally have pagination since the number of scooters could be quite large.
* We would probably want to have sorting options for the <code>/available</code> endpoint (most recent returned, closest, last cleaned, etc.)
* I disabled csrf for the post endpoints. In a production environment, we would not do that. We would also have SSL certifications.
* Since we're dealing with coordinates, we might want to use a Spatial database so that the coordinate queries are more efficient.
* I have </code>/reserve</code> and </code>/end_reservations</code>. It might make sense to just have </code>/reservations</code> where POST creates and DELETE ends a reservation. The same method can be applied with the </code>/pay</code> and </code>/calc_payment</code> where instead we would do a GET or a POST to <code>/payments</code>to differentiate accordingly. Ideally, the model would get restructured for that, which requires a clearer definition of what a payment is and what needs to be tracked. A GET could just return the estimate (without creating an object) and a POST with additional data, would store the payment amount, the rate, time of payment and additional data needed. The current payment model a small mock example.
