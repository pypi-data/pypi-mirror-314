import factory

from sage_templater.schemas import SmallBoxRecordSchema


class SmallBoxRecordSchemaFactory(factory.Factory):
    class Meta:
        model = SmallBoxRecordSchema

    code = factory.Faker("ean8")
    national_id = factory.Faker("ssn")
    verification_digit = factory.Faker("numerify", text="##")
    name = factory.Faker("name")
    invoice = factory.Faker("ean13")
    date = factory.Faker("date")
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    tax = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    description = factory.Faker("sentence")
    source_file = factory.Faker("file_path")
    source_sheet = factory.Faker("word")
