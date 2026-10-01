from datetime import datetime
from apps.processing.cleaner import REQUIRED_FIELDS


def validate_record(record):
    reasons = []

    if not isinstance(record, dict):
        return False, ["Record is not a dictionary"]

    for field in REQUIRED_FIELDS:
        if field not in record:
            reasons.append(f"Missing field: {field}")

    if not record.get("id"):
        reasons.append("ID is empty")

    if not record.get("title"):
        reasons.append("Title is empty")

    if not record.get("source"):
        reasons.append("Source is empty")

    if not record.get("url"):
        reasons.append("URL is empty")

    if record.get("published_at"):
        try:
            datetime.strptime(
                record["published_at"],
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            try:
                datetime.strptime(
                    record["published_at"],
                    "%Y-%m-%d"
                )
            except ValueError:
                reasons.append("Invalid published_at format")

    return len(reasons) == 0, reasons


def validate_records(records):
    valid_records = []
    invalid_records = []

    for record in records:
        is_valid, reasons = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            invalid_records.append({
                "record": record,
                "reasons": reasons
            })

    return valid_records, invalid_records