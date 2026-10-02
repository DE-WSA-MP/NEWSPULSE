def integrate_records(*record_lists):

    integrated_records = []

    for records in record_lists:
        if not records:
            continue

        integrated_records.extend(records)

    return integrated_records