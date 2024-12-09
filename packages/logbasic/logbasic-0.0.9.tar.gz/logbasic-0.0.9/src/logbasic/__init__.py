import datetime as dt
import inspect
import json
import os
from typing import Any, Final

from .color_code import ColorCode
from .log_type_text import LogTypeText

DEBUGGING = False  # set either via this variable or via env var 'log_debugging'
LOG_DEBUGGING_ENV_VAR: Final = 'log_debugging'


def in_debugging() -> bool:
    return bool(os.environ.get(LOG_DEBUGGING_ENV_VAR, '')) or DEBUGGING


####################
# COMMON FUNCTIONS #
####################


def debug(*args: object) -> None:
    if in_debugging():
        format_and_print(ColorCode.grey, LogTypeText.debug, *args)


def info(*args: object) -> None:
    format_and_print(ColorCode.reset, LogTypeText.info, *args)


def warning(*args: object) -> None:
    format_and_print(ColorCode.yellow, LogTypeText.warning, *args)


def error(*args: object) -> None:
    format_and_print(ColorCode.bold_red, LogTypeText.error, *args)


def success(*args: object) -> None:
    """
    When some process has succesfully finished. E.g. "Finished uploading to the database!"
    """
    format_and_print(ColorCode.green, LogTypeText.success, *args)


def special(*args: object) -> None:
    """
    When you want to be able to see this line of code especially well. Useful for debugging when there are already lots of print statements.
    """
    format_and_print(ColorCode.purple_marked, LogTypeText.special, *args)


#####################################
# FUNCTIONS TO GET FORMATTED STRING #
#####################################


def debug_string(*args: object) -> None:
    if in_debugging():
        format(ColorCode.grey, LogTypeText.debug, *args)


def info_string(*args: object) -> None:
    format(ColorCode.reset, LogTypeText.info, *args)


def warning_string(*args: object) -> None:
    format(ColorCode.yellow, LogTypeText.warning, *args)


def error_string(*args: object) -> None:
    format(ColorCode.bold_red, LogTypeText.error, *args)


def special_string(*args: object) -> None:
    format(ColorCode.purple_marked, LogTypeText.special, *args)


def success_string(*args: object) -> None:
    format(ColorCode.green, LogTypeText.success, *args)


# Helper Functions


def format_and_print(color: ColorCode, log_type_text: LogTypeText, *args: object):
    print(format(color, log_type_text, *args))


def format(color: ColorCode, log_type_text: LogTypeText, *args: object):
    args_string = convert_args_to_str(*args)
    # time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # only want milliseconds so remove 3 last nums form nanoseconds
    time = format_datetime(dt.datetime.now())

    og_function_stack = inspect.stack()[3]
    function = og_function_stack[3]
    function = f'\\{function}()' if function != '<module>' else ''
    # \ for windows, / for linux
    file = og_function_stack[1].rsplit('\\', 1)[-1].rsplit('/', 1)[-1]

    time_part = ColorCode.grey.add_to(time)
    log_type_part = color.add_to(f'[{log_type_text.value}]')
    added_space = ' ' * (log_type_text.n_max_chars - log_type_text.n_chars)
    file_function_part = ColorCode.grey.add_to(f'{file}{function}:')

    formatted_string = f'{time_part} {log_type_part} {added_space}{file_function_part}{color.add_to(args_string)}'

    return formatted_string


def convert_args_to_str(*args: object) -> str:
    result: str = ''
    for i in range(0, len(args)):
        arg = args[i]

        str_arg: str = format_on_type(arg)

        if i == 0:
            result = result + str_arg
        else:
            result = result + ' ' + str_arg
    return result


def format_on_type(arg: Any) -> str:
    if isinstance(arg, dict):
        result = format_dict(arg)
    elif isinstance(arg, dt.datetime):
        result = format_datetime(arg)
    elif isinstance(arg, dt.timedelta):
        result = format_timedelta(arg)
    else:
        result = str(arg)

    return result


def format_dict(input_dict: dict) -> str:
    try:
        result = json.dumps(input_dict, sort_keys=True, indent=4)
    except Exception:
        result = str(input_dict)
    return result


def format_timedelta(timedelta: dt.timedelta) -> str:
    if timedelta < dt.timedelta(0):
        return '-' + format_timedelta(-timedelta)
    else:
        # Change this to format positive timedeltas the way you want
        # return str(dt.timedelta(days=timedelta.days, seconds=timedelta.seconds))
        # return str(timedelta)
        return format_positive_timedelta(timedelta)


def format_positive_timedelta(timedelta: dt.timedelta) -> str:
    """
    Format the timedelta like this:
    days = int(leftover_time / (3600 * 24))
    leftover_time -= days * (3600 * 24)

    hours = int(leftover_time / 3600)
    leftover_time -= hours * 3600

    minutes = int(leftover_time / 60)
    leftover_time -= minutes * 60

    seconds = int(leftover_time)
    leftover_time -= seconds
    return f'{days}D{hours}H{minutes}M{seconds}S'

    """
    leftover_time = timedelta.total_seconds()

    fittings = [3600 * 24, 3600, 60, 1]  # days, hours, minutes, seconds
    results = [0] * 4

    for i in range(4):
        results[i] = int(leftover_time / fittings[i])
        leftover_time -= results[i] * fittings[i]

    return f'{results[0]}D{results[1]}H{results[2]}M{results[3]}S'

    # leaving the below code to show what the above does:


def format_datetime(datetime: dt.datetime) -> str:
    if datetime.tzinfo is None:
        tz = ''
    else:
        utcoffset: dt.timedelta = datetime.tzinfo.utcoffset(datetime)  # type:ignore
        prefix = '+' if utcoffset.total_seconds() > 0 else '-'
        tz = f'{prefix}{format_timedelta(utcoffset)}' if utcoffset.total_seconds() > 0 else '+UTC'  # type:ignore

    timetuple = datetime.timetuple()

    day_of_the_week_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]]
    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1]
    processed_time_nums = list(map(lambda x: str(x).zfill(2), timetuple))

    return f'{day_of_the_week_name}, {processed_time_nums[2]} {month_name} {processed_time_nums[0]}, {processed_time_nums[3]}:{processed_time_nums[4]}:{processed_time_nums[5]}.{str(int(datetime.microsecond/10000)).zfill(2)}{tz}'
