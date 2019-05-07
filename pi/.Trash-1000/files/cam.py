import cv2
import numpy as np
from oscpy.client import OSCClient

class cam():

    def __init__(self,cam_num,ip,port):
        print ("cam initialized")
        self.osc = OSCClient(ip, port)
        self.range_filter = 'HSV'
        self.sequence_no=1
        self.flag=True
        self.camera = cv2.VideoCapture(cam_num)
        ret, image = self.camera.read()
        if (not ret):
            print("cam error!")
            pass
        (self.height,self.width) = image.shape[:2]
        if (cam_num==5):
            self.flip=True
            self.m1v1_min, self.m1v2_min, self.m1v3_min, self.m1v1_max, self.m1v2_max, self.m1v3_max = [155, 6, 0, 170, 255, 255]#[50, 20, 0, 70, 255, 255]
            self.m2v1_min, self.m2v2_min, self.m2v3_min, self.m2v1_max, self.m2v2_max, self.m2v3_max = [50, 7, 0, 78, 255, 255]#[0, 5, 0, 10, 255, 255]
        
        else:
            self.flip=True
            self.m1v1_min, self.m1v2_min, self.m1v3_min, self.m1v1_max, self.m1v2_max, self.m1v3_max = [1, 25, 0, 10, 255, 255]
            self.m2v1_min, self.m2v2_min, self.m2v3_min, self.m2v1_max, self.m2v2_max, self.m2v3_max = [44, 10, 0, 66, 255, 255]
        self.items = [[0,0]] #queue

    def frame(self,*args):
        
        ret, image = self.camera.read()
        if self.flip:
            image = cv2.flip(image, 1)
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(frame_to_thresh, (self.m1v1_min, self.m1v2_min, self.m1v3_min), (self.m1v1_max, self.m1v2_max, self.m1v3_max))
        thresh2 = cv2.inRange(frame_to_thresh, (self.m2v1_min, self.m2v2_min, self.m2v3_min), (self.m2v1_max, self.m2v2_max, self.m2v3_max))
        
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask2 = cv2.morphologyEx(thresh2, cv2.MORPH_OPEN, kernel)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
            if len(cnts2) > 0:
                cx = max(cnts2, key=cv2.contourArea)
                ((x, y), radius2) = cv2.minEnclosingCircle(cx)
            else:
                radius2=0
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
            if radius > 25:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                
                c1,c2=self.setCursorPos(int(x1),int(y1),int(self.x),int(self.y))
                
                if (len(cnts2)>0) and (radius2 > 25):
                    c1,c2 = c1/self.width , c2/self.height
                    self.osc.send_message(b'/tuio/2Dcur',(b'alive',self.sequence_no))
                    self.osc.send_message(b'/tuio/2Dcur',(b'set',self.sequence_no,c1,c2))
                    self.flag=True
                    

                    
                
                else:
                    if self.flag:
                        if (self.sequence_no<99999):
                            self.sequence_no=self.sequence_no+1
                        else:
                            self.sequence_no=1
                        
                        self.flag=False
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
    a=cam(0,'192.168.43.1',3334)
    while True:
        a.frame()
