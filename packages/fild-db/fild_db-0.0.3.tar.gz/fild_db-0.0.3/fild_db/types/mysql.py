import json

from fild.sdk import Array, Bool, Dictionary


class DbBool(Bool):
    def to_db(self):
        return int(self.value)

    def with_values(self, values):
        if isinstance(values, int):
            values = bool(values)

        self._value = values

        return self


class DBJsonDict(Dictionary):
    def to_db(self):
        return json.dumps(self.value, separators=(',', ':'))

    def with_values(self, values):
        if isinstance(values, str):
            values = json.loads(values)

        if values is not None:
            return super().with_values(values)

        return self


class DbJsonArray(Array):
    def to_db(self):
        return json.dumps(self.value, separators=(',', ':'))

    def with_values(self, values):
        if isinstance(values, str):
            values = json.loads(values)

        if values is not None:
            return super().with_values(values)

        return self
