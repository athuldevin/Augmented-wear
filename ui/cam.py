# python cam.py --filter HSV --webcam

import cv2
import argparse
import numpy as np
import pyautogui


(screen_width,screen_height) = pyautogui.size()

def callback(value):
    pass


def main():

    range_filter = 'HSV'

    camera = cv2.VideoCapture(0)


    while True:
        
        ret, image = camera.read()
        image = cv2.flip(image, 1)
        (height, width) = image.shape[:2]
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = [0, 84, 136, 38, 255, 255]

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
 
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                #pyautogui.moveTo(int(x)*(screen_width/width), int(y)*(screen_height/height))
                pyautogui.dragTo(int(x)*(screen_width/width), int(y)*(screen_height/height),.3, button='left')

                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
 
        # show the frame to our screen
        cv2.imshow("Original", image)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            
            break


if __name__ == '__main__':
    main()
