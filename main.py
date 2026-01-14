import cv2
import os
import time



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



def frame_resizer(frame, max_height=500, *max_width):
    
    height, width, _ = frame.shape
    aspect_ratio = width/height
    
    if max_width:
        new_width = max_width
        new_height = int(new_width/aspect_ratio)
    elif max_height:
        new_height = max_height
        new_width = int(aspect_ratio*new_height)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    return resized_frame





def video_player(video_file_path):
    capture = cv2.VideoCapture(video_file_path)
    
    time_start = time.time() 
    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps <=0:
        fps = 30
    frame_duration = 1/fps
    frame_count = 0

    while True:
        ret, frame = capture.read()
        if ret:
            time_expected = time_start + (frame_duration * frame_count)
            time_current = time.time()
            if time_expected > time_current:
                time.sleep(time_expected-time_current)
            cv2.imshow("original",frame)
            if cv2.waitKey(1) & 0xFF==ord("q"):
                cv2.destroyAllWindows()
            frame_count+=1

        else:
            time_end = time.time()
            break
    print(f"total time : {time_end-time_start}")
