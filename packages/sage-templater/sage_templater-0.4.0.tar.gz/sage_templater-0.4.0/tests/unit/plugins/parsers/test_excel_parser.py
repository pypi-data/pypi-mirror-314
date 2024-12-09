from pathlib import Path

import openpyxl
import pytest

from sage_templater.plugins.parsers.excel_parser import (
    clean_raw_rows,
    get_raw_rows,
    get_start_and_end_row_numbers,
    get_wb_and_sheets,
    parse_raw_rows, is_small_box_template,
)


class TestGetWbAndSheets:
    def test_get_wb_and_sheets(self, small_box_xlsx_c1) -> None:
        wb, sheets = get_wb_and_sheets(small_box_xlsx_c1)
        assert isinstance(wb, openpyxl.Workbook)
        expected_sheets = [
            "14 DE ENERO ",
            "31 DE ENERO",
            "26 DE FEBRERO",
            "1 DE ABRIL",
            "2 DE MAYO",
            "1 DE JUNIO",
            "29 DE JUNIO",
            "COLOMBIA JUL19",
            "REEMBOLSO",
            "29 DE JULIO",
            "2 DE SEPTIEMBRE",
            "30 DE SEPTIEMBRE",
            "30 DE OCTUBRE",
            "COLOMBIA NOV19",
            "Hoja1",
            "30 DE NOVIEMBRE",
            "30 DE DICIEMBRE",
            "31 DE ENERO 2019",
            "29 DE FEBRERO 2020",
            "MARZO",
            "ABRIL",
            "MAYO",
            "VI\u00c1TICO OSVALDO",
            "VI\u00c1TICO FARIEL",
            "JUNIO ",
            "JULIO",
            "AGOSTO",
            "SEPTIEMBRE",
            "OCTUBRE",
            "NOVIEMBRE",
            "DICIEMBRE",
            "ENERO 2021",
            "FEBRERO 2021",
            "MARZO 2021",
            "ABRIL 2021",
            "MAYO 2021",
            "JUNIO 2021",
            "JULIO 2021",
            "AGOSTO 2021",
        ]

        assert sheets == expected_sheets


class TestGetStartAndEndRowNumbers:
    @pytest.mark.parametrize(
        "sheet_name, expected_start_row, expected_end_row",
        [
            ("14 DE ENERO ", 10, 42),
            ("31 DE ENERO", 10, 47),
            ("26 DE FEBRERO", 10, 39),
            ("1 DE ABRIL", 10, 57),
            ("2 DE MAYO", 10, 47),
            ("1 DE JUNIO", 10, 60),
            ("29 DE JUNIO", 10, 48),
            ("COLOMBIA JUL19", 10, 26),
            ("REEMBOLSO", 10, 18),
            ("29 DE JULIO", 10, 48),
            ("2 DE SEPTIEMBRE", 10, 46),
            ("Hoja1", -1, 1),
        ],
    )
    def test_get_start_and_end_row_numbers(
        self, sheet_name, expected_start_row, expected_end_row, small_box_xlsx_c1
    ) -> None:
        wb, sheets = get_wb_and_sheets(small_box_xlsx_c1)
        start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
        assert start_row == expected_start_row, f"Expected {expected_start_row} but got {start_row} for {sheet_name}"
        assert end_row == expected_end_row, f"Expected {expected_end_row} but got {end_row} for {sheet_name}"

    @pytest.mark.parametrize("only_visible, count", [
        (True, 7),
        (False, 8)
    ])
    def test_get_start_and_end_row_numbers_hidden_sheets(self,only_visible, count, sage_folder) -> None:
        xl_file = sage_folder / 'data_dc/2023/5. Mayo/Cajas menudas/CAJA MENUDA CHIRIQUI OPERACIONES MAYO 2023.xlsx'
        wb, sheets = get_wb_and_sheets(xl_file, only_visible=only_visible)
        assert len(sheets) == count

class TestGetRawRows:
    def test_get_raw_rows(self, small_box_xlsx_c1) -> None:
        wb, sheets = get_wb_and_sheets(small_box_xlsx_c1)
        start_row, end_row = get_start_and_end_row_numbers(wb, "14 DE ENERO ")
        raw_rows = get_raw_rows(wb, "14 DE ENERO ", start_row, end_row)
        assert len(raw_rows) == end_row - start_row + 1


class TestCleanRawRows:
    def test_clean_raw_rows(self, small_box_xlsx_c1) -> None:
        wb, sheets = get_wb_and_sheets(small_box_xlsx_c1)
        sheet_name = "14 DE ENERO "
        start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
        raw_rows = get_raw_rows(wb, sheet_name, start_row, end_row)
        cleaned_raw_rows = clean_raw_rows(raw_rows)

        assert len(cleaned_raw_rows) == 23


class TestParseRawRows:
    def test_parse_raw_rows(self, small_box_xlsx_c1) -> None:
        wb, sheets = get_wb_and_sheets(small_box_xlsx_c1)
        sheet_name = "14 DE ENERO "
        start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
        raw_rows = get_raw_rows(wb, sheet_name, start_row, end_row)
        records = parse_raw_rows(raw_rows, small_box_xlsx_c1, sheet_name, has_headers=True)
        assert len(records) == 23
        assert records[0].source_file == str(small_box_xlsx_c1)
        assert records[0].source_sheet == sheet_name

    def test_tmp(self):
        xl_file = Path(
            "/home/luiscberrocal/PycharmProjects/sage-templater/tests/fixtures/CAJA MENUDA OPERACIONES gerencia dic 2021.xlsx"
        )
        wb, sheets = get_wb_and_sheets(xl_file)
        sheet_name = "COLOMBIA NOV19"
        start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
        raw_rows = get_raw_rows(wb, sheet_name, start_row, end_row)
        records = parse_raw_rows(raw_rows, xl_file, sheet_name, has_headers=True)
        assert len(records) == 9

    def test_tmp2(self):
        xl_file = Path(
            "/home/luiscberrocal/Downloads/sage/data_dc/2021/Diciembre/CAJA MENUDA 2021 COMPRAS JENNY DIC 30.xlsx"
        )
        wb, sheets = get_wb_and_sheets(xl_file)
        sheet_name = "II enero "
        start_row, end_row = get_start_and_end_row_numbers(wb, sheet_name)
        raw_rows = get_raw_rows(wb, sheet_name, start_row, end_row)
        clean_rows = clean_raw_rows(raw_rows)
        records = parse_raw_rows(clean_rows, xl_file, sheet_name)
        assert len(records) == 28

    def test_error(self, sage_folder):
        xl_file = sage_folder / 'data_ls/Año 2023/Estados Financieros Formateados Logic Studio 2023 - auditoría.xlsx'


class TestIsSmallBoxTemplate:
    def test_is_small_box_template(self, small_box_xlsx_c1) -> None:
        assert is_small_box_template(small_box_xlsx_c1)

    def test_error(self, sage_folder):
        xl_file = sage_folder / 'data_ls/Año 2023/Estados Financieros Formateados Logic Studio 2023 - auditoría.xlsx'
        assert not is_small_box_template(xl_file)

    def test_error2(self, sage_folder):
        # /home/luiscberrocal/Downloads/sage/data_dc/2023/5. Mayo/Cajas menudas/CAJA MENUDA CHIRIQUI OPERACIONES MAYO 2023.xlsx
        xl_file = sage_folder / 'data_dc/2023/5. Mayo/Cajas menudas/CAJA MENUDA CHIRIQUI OPERACIONES MAYO 2023.xlsx'
        assert is_small_box_template(xl_file)
