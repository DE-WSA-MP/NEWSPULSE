def integrate_records(*record_lists):
    """
    Combine records from multiple NewsPulse sources.

    The function accepts any number of lists containing
    NewsPulse records and combines them into one list.
    """

    integrated_records = []

    for records in record_lists:
        if not records:
            continue

        integrated_records.extend(records)

    return integrated_records