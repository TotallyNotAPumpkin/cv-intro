import cv2
from matplotlib import pyplot as plt
import numpy as np
import lane_detection
import lane_following

def videoDetection(vid):
    output_video = cv2.VideoWriter('output_videoo.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (1912, 535))
    # video.release() #Save video to disk.
    # total_frames = []
    # Capture frame-by-frame
    count = 1
    while True:
        ret, frame = vid.read()
        if ret:
            resized = (cv2.resize(frame, (1912, 1069)))
            h = resized.shape[0]
            w = resized.shape[1]
            againResized = resized[int(h/2) : h, 0 : w]
        
            lines = lane_detection.detect_lines(againResized, 30, 100, 3, 229, 13)
            if lines is not None:
                lanes = lane_detection.detect_lanes(againResized, lines)
            else:
                lanes = []
            frame = lane_detection.draw_lanes(againResized, lanes)
            # total_frames.append(frame)
            output_video.write(frame)
        print(count)
        count += 1
        if count >= vid.get(cv2.CAP_PROP_FRAME_COUNT): break # NOTE TO CHECK THIS OVER BECAUSE I DUNNO IF ITS >= OR ==
    output_video.release()

if __name__ == "__main__":
    vid = cv2.VideoCapture('AUV_Vid.mkv')
    videoDetection(vid)
