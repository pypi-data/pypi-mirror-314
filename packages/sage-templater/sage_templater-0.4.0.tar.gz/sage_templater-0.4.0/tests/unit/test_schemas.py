from decimal import Decimal

import pytest

from sage_templater.schemas import SmallBoxRecordSchema
from tests.factories import SmallBoxRecordSchemaFactory


class TestSmallBoxRecordSchema:
    def test_create(self):
        schema = SmallBoxRecordSchemaFactory.create()
        assert schema
        schema_dict = schema.model_dump()

    @pytest.mark.parametrize(
        "tax",
        [
            "None",
            "",
        ],
    )
    def test_tax_zero_defaults(self, tax):
        schema_dict = {
            "code": "71570723",
            "national_id": "689-05-2348",
            "verification_digit": "63",
            "name": "Donna Nolan",
            "invoice": "6174137190515",
            "date": "2010-08-30",
            "amount": "7215.15",
            "tax": tax,
            "total": "1777.70",
            "description": "Machine speech edge military piece role thus.",
            "source_file": "/agree/edge.mp3",
            "source_sheet": "security",
        }
        schema = SmallBoxRecordSchema(**schema_dict)
        assert schema.tax == Decimal("0.0")
