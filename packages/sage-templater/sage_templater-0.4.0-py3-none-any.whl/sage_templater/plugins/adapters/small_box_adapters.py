from pathlib import Path

import pandas as pd

from sage_templater.exceptions import SageParseRawError
from sage_templater.plugins.parsers.excel_parser import get_wb_and_sheets, get_start_and_end_row_numbers, get_raw_rows, \
    parse_raw_rows
from sage_templater.schemas import SmallBoxRecordSchema, SmallBoxSageRecordSchema


def export_small_box_sage_record(record: SmallBoxRecordSchema, reference: str) -> SmallBoxSageRecordSchema:
    """Export a small box record to a Sage record."""
    description = (f"{record.name} ruc {record.national_id} dv {record.verification_digit} "
                   f"fact: {record.invoice} {record.description}")
    return SmallBoxSageRecordSchema(
        date=record.date,
        reference=reference,
        description=description,
        amount=record.total,
        account="",
        distribution_number=1,
    )


def from_small_box_excel_to_dataframe(excel_file: Path) -> tuple[pd.DataFrame, list[dict]]:
    """Read a small box excel file and return a dataframe."""
    wb, sheets = get_wb_and_sheets(excel_file)
    total_records = []
    sheets_with_errors = []
    for sheet_name in sheets:
        try:
            start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
            raw_rows = get_raw_rows(wb, sheet_name, start_row, end_row)
            records = parse_raw_rows(raw_rows, excel_file, sheet_name, has_headers=True)
            total_records.extend(records)
        except SageParseRawError as e:
            sheets_with_errors.append({"sheet_name": sheet_name, "error": str(e), "file": str(excel_file)})
    final_records = [r.model_dump() for r in total_records]
    return pd.DataFrame.from_records(final_records), sheets_with_errors
