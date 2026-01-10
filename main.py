import cv2
import os

def read_files(directory_name = "media_files", all_file_type = False, file_type="mp4"):
    all_files_path = []
    current_path = os.getcwd()
    media_directory_path = os.path.join(current_path, directory_name)
    
    if not  os.path.isdir(media_directory_path):
        raise FileNotFoundError("directory not found")

    for file in os.listdir(media_directory_path):
        file_path = os.path.join(media_directory_path, file)
        
        if not os.path.isfile(file_path):
            continue
        
        if not all_file_type:
            _, extention = os.path.splitext(file)
            if extention.lower() != f".{file_type.lower()}":
                continue
        
        all_files_path.append(file_path)


    return all_files_path



print(read_files())