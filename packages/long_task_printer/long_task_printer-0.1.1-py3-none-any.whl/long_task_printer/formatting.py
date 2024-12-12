def format_time(time):
    """
    Formats the given time in seconds to something human readable. Examples:

    - 1 second:      1.00s
    - 0.123 seconds: 123.00ms
    - 100 seconds:   01m:40s
    - 101.5 seconds: 01m:41s
    - 3661 seconds:  01h:01m:01s
    """
    if time is None:
        return "?s"

    if time < 1:
        return f"{format_float(round(time * 1000, 2))}ms"
    elif time < 60:
        return f"{format_float(round(time, 2))}s"
    elif time < 3600:
        minutes = int(time) // 60
        seconds = int(time - minutes * 60)
        return f"{format_int(minutes)}m:{format_int(seconds)}s"
    else:
        hours = int(round(time) // 3600)
        minutes = int((round(time) % 3600) / 60)
        seconds = int((time - (hours * 3600 + minutes * 60)))
        return f"{format_int(hours)}h:{format_int(minutes)}m:{format_int(seconds)}s"


def format_int(value):
    return "{:02d}".format(value)


def format_float(value):
    return "{:.02f}".format(value)
