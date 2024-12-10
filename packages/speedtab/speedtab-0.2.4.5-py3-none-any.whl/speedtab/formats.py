from abc import ABC
from typing import Union


class Color:
    def __init__(self, input: Union[str, tuple] = ()):
        if isinstance(input, str):
            input = tuple(int(input.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        self.color = dict([(key, color / 255) for key, color in zip(('red', 'green', 'blue'), input + (0,) * 3)])


class BaseNumberFormat(ABC):
    def __init__(self, type, pattern):
        self.fields = 'userEnteredFormat(numberFormat)'
        self.cell = {'userEnteredFormat': {'numberFormat': {'type': type, 'pattern': pattern}}}


class Number(BaseNumberFormat):
    def __init__(self, pattern: str = '0'):
        super().__init__('NUMBER', pattern)


class Dollar(BaseNumberFormat):
    def __init__(self, pattern: str = '$#,##0'):
        super().__init__('CURRENCY', pattern)


class Percent(BaseNumberFormat):
    def __init__(self, pattern: str = '0%'):
        super().__init__('PERCENT', pattern)


class Date(BaseNumberFormat):
    def __init__(self, pattern: str = 'yyyy-mm-dd'):
        super().__init__('DATE', pattern)


class Time(BaseNumberFormat):
    def __init__(self, pattern: str = 'hh:mm:ss'):
        super().__init__('TIME', pattern)


class Text(BaseNumberFormat):
    def __init__(self, pattern: str = None):
        super().__init__('TEXT', pattern)


class DateTime(BaseNumberFormat):
    def __init__(self, pattern: str = 'yyyy-mm-dd hh:mm:ss'):
        super().__init__('DATE_TIME', pattern)


class Scientific(BaseNumberFormat):
    def __init__(self, pattern: str = '0.00E+00'):
        super().__init__('SCIENTIFIC', pattern)


class Border:
    def __init__(self, style: str, width: int, color: Color):
        self.style = style
        self.width = width
        self.color = color.color
