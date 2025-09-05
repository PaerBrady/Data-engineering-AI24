# ELT/setup.py
import os
from pathlib import Path 

# Basera allt på DATA_DIR (default /app/Data)
base_dir = Path(os.getenv("DATA_DIR", Path(__file__).parents[1] / "Data"))

paths_directory = {
    "users":  base_dir / "datalake" / "users",
    "data_warehouse": base_dir / "data_warehouse",
    "avatars": base_dir / "data_warehouse" / "avatars",
}

def setup_folder_structure():
    for path in paths_directory.values():
        path.mkdir(parents=True, exist_ok=True)