from pytz import timezone

from fild.sdk import Field, dates


class DbTimestamp(Field):
    def generate_value(self):
        return dates.generate_time()

    def to_db(self):
        return self.value

    def to_format(self, fmt=dates.Pattern.DATE):
        return self.value.strftime(fmt)

    def to_timezone(self, tz):
        return self.value.astimezone(tz=timezone(tz))
