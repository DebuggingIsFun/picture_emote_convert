import os
import glob
from dotenv import load_dotenv, set_key
from PIL import Image

####
preferences_env="preferences.env"
soruceImagePath=""
sourceImageList = []
output_folder= ""
sourceImageName = []
dimension28 = (28,28)
dimension56 = (56,56)
dimension112 = (112,112)

if os.path.exists(preferences_env):
    print(f"Found saved preferences in {preferences_env}")
    load_dotenv(preferences_env)
    soruceImagePath=os.getenv("SOURCE_IMAGE_PATH")
    output_folder=os.getenv("OUTPUT_FOLDER")
    print("========Loaded Preferences============")
    print(f"Source Path {soruceImagePath}")
    print(f"Output Path {output_folder}")
    print()
    choice = input("Press C to change paths, or anything else to process images: [ENTER Requierd]").strip().upper()

    if choice == "C":
        soruceImagePath = input("Source path e.g. C:/Users/username/Pictures/tobetested for Windows or for Unix based Sysstems /home/user/pictures  : ").strip().replace("\\","/")
        if not soruceImagePath.endswith("/"):
            soruceImagePath +="/*"
        elif not soruceImagePath.endswith("*"):
            soruceImagePath +="*"
        output_folder = input("Destination path z.B. C:/Users/username/Pictures/tobetested/converted for Windows or for Unix based Sysstems /home/user/pictures : ").strip().replace("\\","/")
        if output_folder.endswith("/"):
            output_folder = output_folder[:-1]
        
        save = input("Do you want to save those paths in preferences? (y/n)").strip().upper()
        if save =="y":
            print("saving new preferences")
            set_key(preferences_env,"SOURCE_IMAGE_PATH",soruceImagePath)
            set_key(preferences_env,"OUTPUT_FOLDER", output_folder)
        else:
            print("Will use new Paths only once")


else:
    print("Did not find preferences. Prompt for input")
    soruceImagePath = input("Source path e.g. C:/Users/username/Pictures/tobetested for Windows or for Unix based Sysstems /home/user/pictures  : ").strip().replace("\\","/")
    if not soruceImagePath.endswith("/"):
        soruceImagePath +="/*"
    elif not soruceImagePath.endswith("*"):
        soruceImagePath +="*"
    output_folder = input("Destination path z.B. C:/Users/username/Pictures/tobetested/converted for Windows or for Unix based Sysstems /home/user/pictures : ").strip().replace("\\","/")
    if output_folder.endswith("/"):
        output_folder = output_folder[:-1]
    set_key(preferences_env,"SOURCE_IMAGE_PATH",soruceImagePath)
    set_key(preferences_env,"OUTPUT_FOLDER", output_folder)
    #print("preferences.env created with those values")

for picture in glob.glob(soruceImagePath):
    if picture.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        im=Image.open(picture)
        sourceImageList.append(im)
        sourceImageName.append(os.path.basename(picture))

for i, image in enumerate(sourceImageList):
    new_dir = f"{output_folder}/{os.path.splitext(sourceImageName[i])[0]}"
    print(new_dir)
    os.makedirs(new_dir, exist_ok=True)
    ##### Notes for me 
    #os.path.splitext(sourceImageName[i])[0] - Remove file extension
    #sourceImageName[i] = "photo.jpg"
    #os.path.splitext("photo.jpg") = ("photo", ".jpg") (tuple)
    #[0] = "photo" (just the name, no .jpg)
    #####
    image.save(f"{new_dir}/Original{sourceImageName[1]}")

    resized_image = image.resize(dimension28)
    resized_image.save(f"{new_dir}/28x28{sourceImageName[i]}")

    resized_image = image.resize(dimension56)
    resized_image.save(f"{new_dir}/56x56{sourceImageName[i]}")

    resized_image = image.resize(dimension112)
    resized_image.save(f"{new_dir}/112x112{sourceImageName[i]}")