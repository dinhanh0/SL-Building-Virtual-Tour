import os
from pathlib import Path

# Change this to your folder if needed
folder = Path(__file__).resolve().parent / "images"

# Grab all images and sort them by creation time
files = sorted(
    [f for f in folder.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]],
    key=lambda p: p.stat().st_ctime
)

for i, f in enumerate(files, start=1):
    new_name = f"SL_ALL_{i:03d}{f.suffix.lower()}"
    new_path = folder / new_name
    print(f"{f.name}  ->  {new_name}")
    f.rename(new_path)
