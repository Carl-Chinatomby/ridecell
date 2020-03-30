class InvalidParamError(Exception):
    def __init__(self, code=422, error='Invalid params given'):
        self.status_code = code
        self.error = error
