import cv2
import numpy as np
import matplotlib.pyplot as plt
import lane_detection

def get_lane_center(img, lanes):
    """Find the center of the lane closest to the middle of a list of given lanes
    args: 
        img (image path or np.ndarray): img that lanes come from
        lanes (list): list of lanes [[[x, x, x, x], [x, x, x, x]], ...]
    return: 
        (list): [centerSlope, centerIntercept]
        """
    

    if not isinstance(img, np.ndarray):
        img = cv2.imread(img)
    # find slopes and intercepts of all lines in the lanes
    cenSlopes = []
    cenInters = []
    if lanes is not None:
        for lane in lanes:
            slope, intercept = lane_detection.get_slopes_intercepts(img, lane)
            cenSl = 1/((1/slope[0] + 1/slope[1])/2)
            cenInt = (intercept[0] + intercept[1])/2
            cenSlopes.append(cenSl)
            cenInters.append(cenInt)
        cenInter = sorted(cenInters, key=lambda x: abs(img[1]/2 - x))[0]
        index = cenInters.index(cenInter)
        slInters = [(cenSlopes)[index], (cenInters)[index]]
    return slInters

def recommend_direction(img, center, slope):
    """Recommends the direction that the AUV should move in order to follow a lane
    args:
        center (int or float): center point of intercepts
        slope (int or float): average slope
    return:
        (list): list of suggested strafe and turn direction"""
    
    # width = img.shape[1] / 2
    # if center >= (width - 50) and center <= (width + 50):
    #     direction =  "forward"
    # elif center > 1220:
    #     direction = "right"
    # else:
    #     direction = "left"

    # if slope > 2.5:
    #     turn = "left"
    # if slope < 2.5:
    #     turn = "right"
    # else: 
    #     turn = "don't turn"
    # return [direction, turn]
    width = img.shape[1] / 2
    if center >= (width - 20) and center <= (width + 20) and abs(1/slope) <= 0.1:
        direction =  "drive forward"
        return[direction]
    elif center > (width + 20):
        direction = "strafe right"
        return[direction]
    elif center < (width - 20):
        direction = "strafe left"
        return[direction]
    if center >= (width - 20) and center <= (width + 20) and slope <= -0.5:
        direction = "turn right"
    if center >= (width - 20) and center <= (width + 20) and slope >= 0.5: 
        direction = "turn left"
    return[direction]
    
if __name__ == "__main__":
    image = cv2.imread('lanes.png')
    img = cv2.resize(image, (1912, 1069))
    lines = lane_detection.detect_lines(img, 30, 100, 3, 229, 13)
    lanes = lane_detection.detect_lanes(img, lines)
    center = get_lane_center(img, lanes)
    action = recommend_direction(img, center[0], center[1])
    print(f"Possible lines: {lines}") # [[1415, 531, 1676, 563], [514, 1047, 699, 738], [1441, 573, 1674, 618], [712, 1068, 765, 839], [557, 973, 706, 725]]
    print(f"Possible lanes: {lanes}") # [[[514, 1047, 699, 738], [712, 1068, 765, 839]]]
    print(f"Center slope and intercept: {center}") # [-2.9955124936257014, 606.2985189581832]
    print(f"Recommended action: {action}")