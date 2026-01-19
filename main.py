import cv2
import os
import time
import imutils




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




def frame_resizer(frame, max_height=500, max_width=None):
    if max_width:
        resized_frame = imutils.resize(frame, width=max_width)
    else:
        resized_frame = imutils.resize(frame, height=max_height)

    return resized_frame




def frame_contour(frame, background_subtractor):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (3,3), 0)

    foreground_mask = background_subtractor.apply(frame_blur)

    _, motion_mask_threshold = cv2.threshold(foreground_mask, 200, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    motion_mask_morphology_open = cv2.morphologyEx(motion_mask_threshold, cv2.MORPH_OPEN, kernel, iterations=2)
    motion_mask_morphology_close = cv2.morphologyEx(motion_mask_morphology_open , cv2.MORPH_CLOSE, kernel, iterations=2)

    contour, _ = cv2.findContours(motion_mask_morphology_close, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    return contour




def draw_contour(frame, contour):
    marked_frame = frame.copy()

    lil_contour = 0
    big_contour = 0

    for cnt in contour:
        if cv2.contourArea(cnt) >= 100:
            cv2.drawContours(marked_frame, cnt, -1, (0,255,0), 2)
            big_contour += 1
        else:
            lil_contour += 1
    print(f"lil : {lil_contour}\nbig : {big_contour}")

    return marked_frame
    

    
def centroid(cnt):
    moments = cv2.moments(cnt)
    if moments["m00"] == 0:
        return None
    center_x = int(moments["m10"]/moments["m00"])
    center_y = int(moments["m01"]/moments["m00"])

    return center_x, center_y   




def video_player(video_file_path):
    capture = cv2.VideoCapture(video_file_path)
    
    time_start = time.time() 
    fps = capture.get(cv2.CAP_PROP_FPS)
    if fps <=0:
        fps = 30
    frame_duration = 1/fps
    frame_count = 0

    background_subtractor = cv2.createBackgroundSubtractorKNN(history=200, detectShadows=True)

    while True:
        ret, frame = capture.read()
        if ret:
            time_expected = time_start + (frame_duration * frame_count)
            time_current = time.time()
            if time_expected > time_current:
                time.sleep(time_expected-time_current)
        
            frame_resized = frame_resizer(frame)
            contour = frame_contour(frame_resized, background_subtractor)

            frame_contoured = draw_contour(frame_resized, contour)

            cv2.imshow("contour",frame_contoured)
            cv2.imshow("original",frame_resized)
        
            if cv2.waitKey(1) & 0xFF==ord("q"):
                break
            frame_count+=1

        else:
            time_end = time.time()
            break
    cv2.destroyAllWindows()

    print(f"total time : {time_end-time_start}")
