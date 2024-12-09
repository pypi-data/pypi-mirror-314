import warnings
from pathlib import Path
from time import time
from typing import List

import click

from sage_templater.plugins.parsers.excel_parser import is_small_box_template

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def get_excel_files(folder: Path, pattern: str = "**/*.xlsx") -> List[Path]:
    """Get excel files from a folder."""
    return list(folder.glob(pattern))


def main(pattern: str = "menuda"):
    folder = Path.home() / "Downloads" / "sage" #/ "data_ls"
    excel_files = get_excel_files(folder)
    for i, excel_file in enumerate(excel_files):
        try:
            if pattern is not None and pattern in excel_file.name.lower():
                start = time()
                is_small_box = is_small_box_template(excel_file)
                elapsed = time() - start
                if is_small_box:
                    click.secho(f"{i + 1} {excel_file.relative_to(folder)} {is_small_box} time: {elapsed:.2f}", fg="green")
                else:
                    click.secho(f"{i + 1} {excel_file.relative_to(folder)} {is_small_box} time: {elapsed:.2f}", fg="yellow")

        except Exception as e:
            click.secho(f"{i + 1} {excel_file.relative_to(folder)} {e}", fg="red")


if __name__ == '__main__':
    main()
