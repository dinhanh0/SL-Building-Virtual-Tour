import os
from pathlib import Path

# ---------------------------------------
# CONFIGURE YOUR FLOOR FOLDERS HERE
# ---------------------------------------

FLOOR_MAP = {
    "SLFloor0": "SL0",
    "SLFloor1": "SL1",
    "SLFloor2": "SL2",
    "SLFloor3": "SL3",
    "SLFloor1/outside": "Outside",
    "LobbyStairs": "LBST",
    "Stairs": "ST",
    "misc": "MS"
}

# Root project folder (this script should be in the project root)
ROOT = Path(__file__).resolve().parent / "SLFloors"


def rename_images():
    for folder_name, new_prefix in FLOOR_MAP.items():
        folder_path = ROOT / folder_name

        if not folder_path.exists():
            print(f"Folder not found: {folder_path}")
            continue

        print(f"\nProcessing folder: {folder_name}")

        for file in folder_path.iterdir():
            if not file.is_file():
                continue

            name = file.stem  # filename without extension
            ext = file.suffix.lower()

            # Only rename cleanup images
            if "_cleanup" not in name:
                continue

            # Extract number from "SL_ALL_085_cleanup"
            parts = name.split("_")
            num_part = next((p for p in parts if p.isdigit()), None)

            if num_part is None:
                print(f" Skipped (no number): {file.name}")
                continue

            # Construct new filename
            new_name = f"{new_prefix}_{num_part}{ext}"
            new_path = folder_path / new_name

            # Rename
            print(f" {file.name} -> {new_name}")
            file.rename(new_path)

    print("\nDONE  All cleanup files renamed!")


if __name__ == "__main__":
    rename_images()
