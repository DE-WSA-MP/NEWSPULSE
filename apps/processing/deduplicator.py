def deduplicate_records(records):
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