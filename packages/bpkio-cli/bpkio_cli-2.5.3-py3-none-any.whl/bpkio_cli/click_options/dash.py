import functools

import click
from cloup import option, option_group


def dash_options(fn):
    @option_group(
        "DASH MPD filters",
        option(
            "--level",
            "mpd_level",
            help="Level of information to display. 1=Period, 2=AdaptationSet, 3=Representation, 4=Segment Info, 5=Segments",
            type=int,
            default=None,
            callback=validate_level,
        ),
        option(
            "--period",
            "mpd_period",
            help="Extract one or multiple periods (accepts a single integer or a range x:y - the first period has index 1)",
            default=None,
            callback=validate_range,
        ),
        option(
            "--adapt",
            "--adapset",
            "mpd_adaptation_set",
            help="Extract a single adaptation set (mimetype)",
            type=str,
            default=None,
        ),
    )
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


def validate_range(ctx, param, value):
    if value is None:
        return value
    try:
        if ":" in value:
            start, end = map(int, value.split(":"))
            return range(start - 1, end)
        else:
            return range(int(value) - 1, int(value))
    except ValueError:
        raise click.BadParameter(f"'{value}' is not a valid int or range")


def validate_level(ctx, param, value):
    if value is None:
        if ctx.params.get("tree"):
            return 3
        else:
            return 5
    if value not in range(1, 6):
        raise click.BadParameter(f"'{value}' is not a valid level")
    return value
