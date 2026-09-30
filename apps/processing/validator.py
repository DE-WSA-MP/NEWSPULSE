from datetime import datetime
from apps.processing.cleaner import REQUIRED_FIELDS


def validate_record(record):
    """
    Validate one NewsPulse record.

    Returns:
        True  -> record is valid
        False -> record is invalid
    """

    if not isinstance(record, dict):
        return False

    # Check that all required fields exist
    for field in REQUIRED_FIELDS:
        if field not in record:
            return False

    # Required fields should not be empty
    if not record["id"]:
        return False

    if not record["title"]:
        return False

    if not record["source"]:
        return False

    if not record["url"]:
        return False

    # Validate published_at if present
    if record["published_at"]:

        try:
            datetime.strptime(
                record["published_at"],
                "%Y-%m-%d %H:%M:%S"
            )

        except ValueError:

            # Also allow date-only values such as
            # Wikipedia's current format.
            try:
                datetime.strptime(
                    record["published_at"],
                    "%Y-%m-%d"
                )

            except ValueError:
                return False

    return True


def validate_records(records):
    """
    Validate a list of NewsPulse records.

    Returns:
        valid_records
        invalid_records
    """

    valid_records = []
    invalid_records = []

    for record in records:

        if validate_record(record):
            valid_records.append(record)

        else:
            invalid_records.append(record)

    return valid_records, invalid_records