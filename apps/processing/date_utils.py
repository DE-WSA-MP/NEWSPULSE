from datetime import datetime


def convert_unix_timestamp(timestamp):
    if not timestamp:
        return ""

    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError, OSError):
        return ""


def normalize_date(date_string):
    if not date_string:
        return ""

    date_string = str(date_string).strip()

    date_formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%B %d, %Y",
        "%b %d, %Y"
    ]

    for date_format in date_formats:
        try:
            date = datetime.strptime(date_string, date_format)

            if "%H" in date_format:
                return date.strftime("%Y-%m-%d %H:%M:%S")

            return date.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return date_string