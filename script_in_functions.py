import os
import glob
from dotenv import load_dotenv, set_key
from PIL import Image

# === Setup ===
preferences_env = "preferences.env"
sourceImagePath = ""
sourceImageList = []
output_folder = ""
sourceImageName = []
dimension28 = (28, 28)
dimension56 = (56, 56)
dimension112 = (112, 112)


def normalize_source_path(path: str) -> str:
    """Ensure source path ends with /* for glob to work properly."""
    clean_path = path.strip().replace("\\", "/")
    if not clean_path.endswith("/"):
        clean_path += "/*"
    elif not clean_path.endswith("*"):
        clean_path += "*"
    return clean_path


def normalize_output_path(path: str) -> str:
    """Ensure output folder path does not end with a slash."""
    clean_path = path.strip().replace("\\", "/")
    return clean_path[:-1] if clean_path.endswith("/") else clean_path


def save_preferences(source: str, output: str):
    """Save paths to preferences.env file."""
    set_key(preferences_env, "SOURCE_IMAGE_PATH", source)
    set_key(preferences_env, "OUTPUT_FOLDER", output)


def prompt_for_paths():
    """Prompt user for input paths."""
    source = normalize_source_path(
        input("Source path e.g. C:/Users/username/Pictures/tobetested for Windows or for Unix-based Systems /home/user/pictures: ")
    )
    output = normalize_output_path(
        input("Destination path e.g. C:/Users/username/Pictures/tobetested/converted for Windows or for Unix-based Systems /home/user/pictures: ")
    )
    return source, output


# === Main logic ===
if os.path.exists(preferences_env):
    print(f"Found saved preferences in {preferences_env}")
    load_dotenv(preferences_env)

    sourceImagePath = os.getenv("SOURCE_IMAGE_PATH")
    output_folder = os.getenv("OUTPUT_FOLDER")

    print("========Loaded Preferences============")
    print(f"Source Path {sourceImagePath}")
    print(f"Output Path {output_folder}\n")

    choice = input("Press C to change paths, or anything else to process images: [ENTER Required] ").strip().upper()

    if choice == "C":
        sourceImagePath, output_folder = prompt_for_paths()
        save_pref = input("Do you want to save those paths in preferences? (y/n) ").strip().lower()
        if save_pref == "y":
            print("Saving new preferences...")
            save_preferences(sourceImagePath, output_folder)
        else:
            print("Will use new paths only once.")
else:
    print("Did not find preferences. Prompt for input")
    sourceImagePath, output_folder = prompt_for_paths()
    save_preferences(sourceImagePath, output_folder)

# === Image Processing ===
for picture in glob.glob(sourceImagePath):
    if picture.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        im = Image.open(picture)
        sourceImageList.append(im)
        sourceImageName.append(os.path.basename(picture))

for i, image in enumerate(sourceImageList):
    new_dir = f"{output_folder}/{os.path.splitext(sourceImageName[i])[0]}"
    print(new_dir)
    os.makedirs(new_dir, exist_ok=True)
   
    ##### Notes for me 
    # os.path.splitext(sourceImageName[i])[0] - Remove file extension
    # sourceImageName[i] = "photo.jpg"
    # os.path.splitext("photo.jpg") = ("photo", ".jpg") (tuple)
    # [0] = "photo" (just the name, no .jpg)
    #####
    image.save(f"{new_dir}/Original{sourceImageName[i]}")

    for size, label in [(dimension28, "28x28"), (dimension56, "56x56"), (dimension112, "112x112")]:
        resized_image = image.resize(size)
        resized_image.save(f"{new_dir}/{label}{sourceImageName[i]}")
