import enum


class ColorCode(enum.Enum):
    # can combine them with ;
    bold_red = '\x1b[31;1;4m'
    red = '\x1b[31m'
    yellow = '\x1b[33m'
    green = '\x1b[32m'
    lightblue = '\x1b[36m'
    blue = '\x1b[34m'
    purple = '\x1b[35m'
    reset = '\x1b[0m'

    bold = '\x1b[1;20m'
    grey = '\x1b[2;20m'
    italic = '\x1b[3;20m'
    underlined = '\x1b[4;20m'
    marked = '\x1b[7;20m'
    crossedout = '\x1b[9;20m'

    red_marked = '\x1b[41m'
    yellow_marked = '\x1b[43m'
    green_marked = '\x1b[42m'
    lightblue_marked = '\x1b[46m'
    blue_marked = '\x1b[44m'
    purple_marked = '\x1b[45m'
    white_marked = '\x1b[47m'

    def add_to(self, string: str) -> str:
        return self.value + string + ColorCode.reset.value
