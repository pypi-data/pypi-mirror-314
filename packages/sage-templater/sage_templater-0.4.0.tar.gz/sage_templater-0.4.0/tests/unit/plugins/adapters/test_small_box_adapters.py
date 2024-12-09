from sage_templater.plugins.adapters.small_box_adapters import from_small_box_excel_to_dataframe


class TestSmallBoxAdapters:

    def test_from_small_box_excel_to_dataframe(self, small_box_xlsx_c1):
        df, sheets_with_errors = from_small_box_excel_to_dataframe(small_box_xlsx_c1)
        assert df.shape == (828, 12)
        assert len(sheets_with_errors) == 1

        df.to_csv("test.csv", index=False)
