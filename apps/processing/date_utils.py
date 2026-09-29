from datetime import datetime


def convert_unix_timestamp(timestamp):
    """
    Convert a Unix timestamp into a readable date-time string.
    """

    if not timestamp:
        return ""

    try:
        return datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except (TypeError, ValueError, OSError):
        return ""