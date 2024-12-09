import os
import zipfile
from pathlib import Path

from tests.conftest import sage_folder


def unzip_all_files(downloads_folder: Path, target_folder: Path):
    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Iterate over all files in the downloads folder
    for item in os.listdir(downloads_folder):
        if item.endswith('.zip'):
            file_path = os.path.join(downloads_folder, item)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
            print(f"Unzipped: {item}")


if __name__ == '__main__':
    sage_folder= Path.home() / "Downloads" / "sage"
    # Example usage
    d_folder =Path.home() / "Downloads"
    t_folder = sage_folder/"data_dc"/"2023"
    unzip_all_files(d_folder, t_folder)
