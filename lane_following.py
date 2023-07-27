import cv2
import numpy as np
import matplotlib.pyplot as plt
import lane_detection

def get_lane_center(img, lanes):
    if not isinstance(img, np.ndarray):
        img = cv2.imread(img)
    # find slopes and intercepts of all lines in the lanes
    slInters = []
    for lane in lanes:
        slope, intercept = lane_detection.get_slopes_intercepts(img, lane)
        cenSl = (slope[0] + slope[1])/2
        cenInt = (intercept[0] + intercept[1])/2
        slInters.append([cenSl, cenInt])
        # slInters.append([slope, intercept])
    return slInters
    # checks if there is currently a lane in the center
if __name__ == "__main__":
    print(get_lane_center('poollanes.png', lane_detection.detect_lanes('poollanes.png', lane_detection.detect_lines('poollanes.png'))))