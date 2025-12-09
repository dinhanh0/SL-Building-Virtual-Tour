from PIL import Image
from pillow_heif import register_heif_opener
from pathlib import Path

# Enable HEIC reading
register_heif_opener()

# Folder containing your HEIC files
folder = Path(__file__).resolve().parent / "floorplan"

# List all .HEIC files in folder
files = list(folder.glob("*.HEIC"))

for filepath in files:
    try:
        # Open HEIC file
        image = Image.open(filepath)

        # New filename (.jpg)
        new_filename = filepath.with_suffix(".jpg")

        # Convert to RGB and save as JPG
        image.convert("RGB").save(new_filename, "JPEG", quality=95)

        print(f"Converted: {filepath.name} -> {new_filename.name}")

    except Exception as e:
        print(f"Failed to convert {filepath.name}: {e}")
