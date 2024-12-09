import enum
from functools import cached_property


class LogTypeText(enum.Enum):
    error = 'E'
    warning = 'W'
    info = 'I'
    debug = 'D'
    special = '!'
    success = 'S'

    @cached_property
    def n_max_chars(self):
        return max([len(x.value) for x in LogTypeText])

    @property
    def n_chars(self):
        return len(self.value)
