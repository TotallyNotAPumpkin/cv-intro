import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_lines(img, threshold1 = 50, threshold2 = 150, apertureSize = 3, minLineLength = 100, maxLineGap = 10):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
    grayCon = cv2.addWeighted(gray, 2, gray, 0, 0)
    edges = cv2.Canny(grayCon, threshold1, threshold2, apertureSize=apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                    edges,
                    1,
                    np.pi/180,
                    100,
                    minLineLength=minLineLength,
                    maxLineGap=maxLineGap,
            ) # detect lines

    lineList = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            linexy = [x1, y1, x2, y2]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            lineList.append(linexy)
    return lineList

def draw_lines(img, lines, color = (0, 255, 0)):
    image = cv2.imread(img)
    for line in lines:
        cv2.line(image, (line[0], line[1]), (line[2], line[3]), color, 3) 
    return image

def get_slopes_intercepts(img, lines):
    image = cv2.imread(img)
    slopes = []
    intercepts = []
    height = image.shape[0]
    for line in lines:
        slope = (line[1] - line[3]) / (line[0] - line[2])
        slopes.append(slope)
        intercepts.append((height-line[1])/slope + line[0])
    return slopes, intercepts

def detect_lanes(img, lines):
    slopes, intercepts = get_slopes_intercepts(lines)
    lineDict = dict(zip(intercepts, slopes))
    height = cv2.imread(img).shape[0]
    possibleLanes = []

    # taking two points and checking if between them is dark:




# cv2.line(image, start_point, end_point, color, thickness) 
if __name__ == "__main__":
    lines = detect_lines('poollanes.jpg', 250, 270)
    plt.imshow(draw_lines('poollanes.jpg', [[30, 40, 100, 100], [200, 200, 300, 300]]))
    print(lines)