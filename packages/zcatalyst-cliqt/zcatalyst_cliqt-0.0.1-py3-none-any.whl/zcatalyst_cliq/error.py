import json


class CatalystError(Exception):
    def __init__(self, message, code = 1, original_err: Exception = None):
        self._code = code
        self._message = message
        self._original_error = original_err
        Exception.__init__(self, self.to_string())

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def original_error(self):
        return self._original_error

    def to_json(self):
        json_dict = {
            'code': self._code,
            'message': self._message
        }
        return json_dict

    def to_string(self):
        return json.dumps(self.to_json())
    