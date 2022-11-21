import cv2
import numpy as np
import random

def get_center(hsv, lower, upper, color):
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 3:
        c = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)

        if radius > 10:
            return x, y, radius, color
    
    return None


cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)


colors = ['blue', 'yellow', 'green', 'orange']
sequence = random.sample(colors, 3)

green_lower = np.array((21, 121, 110))
green_upper = np.array((81, 181, 150))

blue_lower = np.array((80, 168, 103))
blue_upper = np.array((120, 208, 153))

yellow_lower = np.array((3, 124, 177))
yellow_upper = np.array((43, 164, 197))

orange_lower = np.array((0, 145, 235))
orange_upper = np.array((20, 185, 255))


while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(frame, (21, 21), 0)
    
    key = cv2.waitKey(1)
    if(key == ord('q')):
        break
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    
    green_center = get_center(hsv, green_lower, green_upper)
    blue_center = get_center(hsv, blue_lower, green_upper)
    orange_center = get_center(hsv, orange_lower, orange_upper)
    yellow_center = get_center(hsv, yellow_lower, yellow_upper)
            
    centres = [green_center, blue_center, orange_center, yellow_center]
    
    
    # if (centres[sequence[0]] is not None and centres[sequence[1]] is not None 
    #     and centres[sequence[2]] is not None and centres[must_be_none] is None):
    #     if (centres[sequence[0]] < centres[sequence[1]] 
    #         and centres[sequence[1]] < centres[sequence[2]]):
            
    #         print("It's true!")
            

    if green_center is not None:
        cv2.circle(frame, (int(green_center[0]), int(green_center[1])), int(green_center[2]),
                       (0, 255, 0), 3)
        
    if blue_center is not None:
        cv2.circle(frame, (int(blue_center[0]), int(blue_center[1])), int(blue_center[2]),
                       (255, 0, 0), 3)
    
    if orange_center is not None:
        cv2.circle(frame, (int(orange_center[0]), int(orange_center[1])), int(orange_center[2]),
                       (0, 0, 255), 3)
    
    if yellow_center is not None:
        cv2.circle(frame, (int(yellow_center[0]), int(yellow_center[1])), int(yellow_center[2]),
                       (255, 255, 255), 3)
    

        
    cv2.imshow("Camera", frame)
    
    
cam.release()
cv2.destroyAllWindows()