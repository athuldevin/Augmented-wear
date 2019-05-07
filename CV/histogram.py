import cv2
import numpy as np

def hand_histogram(hsv_frame,mask):
    
    bins = [18, 25]
    hist = cv2.calcHist([hsv_frame], [0, 1], mask, bins, [0, 180, 0, 256])
    cv2.normalize(hist,hist)
    print (hist)
    print (len(hist))
    print (len(hist[0]))
    ind = np.unravel_index(np.argmax(hist, axis=None), hist.shape)
    print (ind)

img = cv2.imread('home.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
hand_histogram(hsv,mask)