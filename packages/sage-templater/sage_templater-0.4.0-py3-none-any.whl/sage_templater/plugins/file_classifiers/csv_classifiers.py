from pathlib import Path
from time import time
from typing import List

import click


def get_csv_files(folder: Path, pattern: str = "**/*.csv") -> List[Path]:
    """Get excel files from a folder."""
    return list(folder.glob(pattern))


def main():
    folder = Path.home() / "Downloads" / "sage"  # / "data_ls"
    csv_files = get_csv_files(folder)
    for i, csv_file in enumerate(csv_files):
        try:
            start = time()
            elapsed = time() - start
            click.secho(f"{i + 1} {csv_file.relative_to(folder)}  time: {elapsed:.2f}", fg="green")

        except Exception as e:
            click.secho(f"{i + 1} {csv_file.relative_to(folder)} {e}", fg="red")


if __name__ == '__main__':
    main()
