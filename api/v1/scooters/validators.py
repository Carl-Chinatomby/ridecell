from decimal import (
    Decimal,
    InvalidOperation,
)

from .exceptions import InvalidParamError


def validate_param(name, value):
    if value is None:
        raise InvalidParamError(error='Invalid value for {}'.format(name))

    try:
        return Decimal(value.strip() if type(value) == str else value)
    except InvalidOperation:
        raise InvalidParamError(error='Invalid value for {}'.format(name))
