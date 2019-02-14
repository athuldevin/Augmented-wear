import cv2
import numpy as np
import pyautogui

class cam():

    def __init__(self,cam_num):
        print ("cam initialized")
        self.range_filter = 'HSV'
        (self.screen_width,self.screen_height) = pyautogui.size()
        self.camera = cv2.VideoCapture(cam_num)
        ret, image = self.camera.read()
        if (not ret):
            print("cam error!")
            pass
        (self.height,self.width) = image.shape[:2]
        if (cam_num==0):
            self.flip=True
            self.v1_min, self.v2_min, self.v3_min, self.v1_max, self.v2_max, self.v3_max = [0, 108, 119, 210, 224, 255]#[0, 103, 147, 19, 222, 255]
        else:
            self.flip=False
            self.v1_min, self.v2_min, self.v3_min, self.v1_max, self.v2_max, self.v3_max = [0, 176, 79, 19, 255, 255]
        self.items = [[0,0]] #queue

    def frame(self,*args):
        
        ret, image = self.camera.read()
        if self.flip:
            image = cv2.flip(image, 1)
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(frame_to_thresh, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
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
            ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            #Store recent points in queue for calculating click or not
            if (len(self.items)<7):
                self.enqueue([int(self.x),int(self.y)])
            else:
                self.dequeue()
                self.enqueue([int(self.x),int(self.y)])

            #Avarage points of queue
            x1,y1=self.avgPoint()
                   
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(image, (int(self.x), int(self.y)), int(radius),(0, 255, 255), 2)
                #c1=((int(x1)+int(self.x))*(self.screen_width/self.width))/2
                #c2=((int(y1)+int(self.y))*(self.screen_width/self.width))/2
                c1,c2=self.setCursorPos(int(x1)*(self.screen_width/self.width),int(y1)*(self.screen_width/self.width),int(self.x)*(self.screen_width/self.width),int(self.y)*(self.screen_width/self.width))
                if (self.dist(self.items[-2][0],self.items[-2][1],int(self.x),int(self.y))<5):
                    pyautogui.mouseDown(c1,c2, button='left')
                #pyautogui.moveTo(int(x)*(screen_width/width), int(y)*(screen_height/height))
                else:
                    pyautogui.mouseUp(c1,c2, button='left')
                    #pyautogui.dragTo(int(x)*(screen_width/width), int(y)*(screen_height/height),(1/20), button='left')
                    

                #cv2.circle(image, center, 3, (0, 0, 255), -1)
                #cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                #cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
        
        # show the frame to our screen
        #cv2.imshow("Original", image)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Mask", mask)
    def dist(self,x1,y1,x2,y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    def setCursorPos( self, pyp0,pyp1,yc0,yc1):
        yp=[0,0]
        if abs(yc0-pyp0)<5 and abs(yc1-pyp1)<5:
            yp[0] = yc0 + .7*(pyp0-yc0) 
            yp[1] = yc1 + .7*(pyp1-yc1)
        else:
            yp[0] = yc0 + .1*(pyp0-yc0)
            yp[1] = yc1 + .1*(pyp1-yc1)
        
        return yp[0],yp[1]

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def avgPoint(self):
        a,b=0,0
        for x,y in self.items:
            a=a+x
            b=b+y
        return a/len(self.items),b/len(self.items)

if __name__ == '__main__':
    a=cam()
    while True:
        a.frame()
