# -*- coding: UTF-8 -*-
import datetime
from dateutil.parser import parse
from . import base


class StringField(base.Field):
    def to_python(self, value):
        if isinstance(value, unicode):
            return value

        if value is None:
            return None
        return unicode(value)


class DateTimeField(base.Field):
    def to_python(self, value):
        if isinstance(value, datetime.datetime):
            return value

        if value is None or value == '':
            return None
        try:
            return parse(value)
        except Exception:
            raise base.BillomatValidationException(
                'invalid value for datetime field (%s): "%s"' % (
                    self.name,
                    value,
                )
            )

    def to_json(self):
        if self.value:
            return self.value.strftime('%Y-%m-%dT%H%i%s')
        return None


class DateField(base.Field):
    def to_python(self, value):
        if isinstance(value, datetime.date):
            return value

        if value is None or value == '':
            return None
        try:
            return parse(value).date()
        except Exception:
            raise base.BillomatValidationException(
                'invalid value for datetime field (%s): "%s"' % (
                    self.name,
                    value,
                )
            )

    def to_json(self):
        if self.value:
            return self.value.strftime('%Y-%m-%d')
        return None


class EmailField(StringField):
    pass


class URLField(StringField):
    pass


class BooleanField(base.Field):
    def to_python(self, value):
        if isinstance(value, bool):
            return value

        return bool(value)

    def to_json(self):
        if self.value:
            return '1'
        return '0'


class FloatField(base.Field):
    def to_python(self, value):
        if isinstance(value, float):
            return value

        if value == self.EMPTY_VALUE:
            if self.required:
                raise base.BillomatValidationException(
                    'empty value not allowed (%s)' % (
                        self.name,
                    )
                )
            return value

        try:
            return float(value)
        except (TypeError, ValueError):
            raise base.BillomatValidationException(
                'invalid value for float field (%s): "%s"' % (
                    self.name,
                    value,
                )
            )


class IntegerField(base.Field):
    def to_python(self, value):
        if isinstance(value, int):
            return value

        if value == self.EMPTY_VALUE:
            if self.required:
                raise base.BillomatValidationException(
                    'empty value not allowed (%s)' % (
                        self.name,
                    )
                )
            return value

        try:
            return int(value)
        except (TypeError, ValueError):
            raise base.BillomatValidationException(
                'invalid value for integer field (%s): "%s"' % (
                    self.name,
                    value,
                )
            )


class ListOfFloatField(base.Field):
    def to_python(self, value):
        return value.split(',')

    def to_json(self):
        return ','.join(self.value)
