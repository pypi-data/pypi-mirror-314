from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def output_folder() -> Path:
    return Path(__file__).parent.parent / "output"


@pytest.fixture(scope="session")
def fixtures_folder() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def small_box_xlsx_c1(fixtures_folder) -> Path:
    return fixtures_folder / "small_box_client1.xlsx"

@pytest.fixture(scope="session")
def sage_folder() -> Path:
    return Path.home() / "Downloads" / "sage"
