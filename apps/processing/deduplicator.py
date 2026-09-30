def deduplicate_records(records):
    """
    Remove duplicate NewsPulse records using a set.

    The record ID is used as the unique key.

    Returns:
        deduplicated_records
    """

    seen_ids = set()
    deduplicated_records = []

    for record in records:

        record_id = record.get("id")

        if not record_id:
            continue

        if record_id in seen_ids:
            continue

        seen_ids.add(record_id)
        deduplicated_records.append(record)

    return deduplicated_records