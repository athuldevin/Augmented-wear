import cv2
import numpy as np
from oscpy.client import OSCClient
import socket
import threading
import time

class cam():

    def __init__(self,cam_num,ip,port,coordinates):
        print ("cam initialized")
        self.x1,self.y1,self.x2,self.y2 = coordinates
        self.osc = OSCClient(ip, port)
        self.range_filter = 'HSV'
        self.capture = False
        self.lock = threading.Lock()
        self.camera = cv2.VideoCapture(cam_num)
        ret, image = self.camera.read()
        if (not ret):
            print("cam error!")
            pass
        self.width,self.height = self.x2-self.x1, self.y2-self.y1
        
        #Markers
        self.flip=False
        self.m1 = [44, 99, 0, 84, 255, 255]
        self.m2 = [0, 174, 0, 6, 255, 255]
        self.m3 = [108, 44, 0, 137, 255, 255]
        self.m4 = [0, 174, 0, 6, 255, 255]
        self.items1 = [[0,0]] #queue1
        self.items2 = [[0,0]] #queue2
        self.seq1 = 2500 #sequence number1
        self.seq2 = 1 #sequence number2
        self.flag1, self.flag2 = False, False

    def touch(self, image, seq, seq2, m1, m2, items, flag):
        # Converting image between thresh hold values
        thresh = cv2.inRange(image, (m1[0], m1[1], m1[2]), (m1[3], m1[4], m1[5]))
        thresh2 = cv2.inRange(image, (m2[0], m2[1], m2[2]), (m2[3], m2[4], m2[5]))
        #Creating mask by using 5 x 5 matrix, Perform advanced morphoogical transformation
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask2 = cv2.morphologyEx(thresh2, cv2.MORPH_OPEN, kernel)
        #find the countour in the mask 
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #proceed only if atleast one contour is found
        if len(cnts) > 0:
            #find largest countour in the mask
            c = max(cnts, key = cv2.contourArea)
            #assign center of max countour to center of marker
            ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
            # For cropping region of interest
            if (self.x > self.x1 and self.x < self.x2 and self.y > self.y1 and self.y < self.y2):
                self.x = self.x - self.x1
                self.y = self.y - self.y1
                #proceed if second marker is found
                if len(cnts2) > 0:
                    c2 = max(cnts2, key = cv2.contourArea)
                    ((x, y), radius2) = cv2.minEnclosingCircle(c2)
                else:
                    radius2 = 0;
                # Store x, y position in queue for reducing shake
                if len(items) < 7:
                    items.insert(0,[self.x, self.y])
                else:
                    items.pop()
                    items.insert(0,[self.x, self.y])
                # Avarage point in queue
                x1, y1 = self.avgPoint(items)

                #only proceed if radius meets minimum size
                if radius > 10:
                    c1,c2=self.setCursorPos(int(x1),int(y1),int(self.x),int(self.y))
                    if (len(cnts2)>0) and (radius2 > 10):
                        c1,c2 = c1/self.width , c2/self.height
                        self.osc.send_message(b'/tuio/2Dcur',(b'alive',seq, seq2))
                        self.osc.send_message(b'/tuio/2Dcur',(b'set',seq,c1,c2))
                        flag=True
                    else:
                        if flag:
                            if (seq<99999):
                                seq=seq+1
                            else:
                                seq=1
                            print (seq)
                            flag=False
        return seq,items,flag
    
    def capture_pic(self,image):
        while self.capture:
            #going to detect is 4 markers present in image if not try another frame
            kernel = np.ones((5,5),np.uint8)
            thresh = cv2.inRange(image, (self.m1[0], self.m1[1], self.m1[2]), (self.m1[3], self.m1[4], self.m1[5]))
            mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            if len(cnts) > 0:
                c = max(cnts, key = cv2.contourArea)
                ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
                if radius > 10:
                    thresh = cv2.inRange(image, (self.m2[0], self.m2[1], self.m2[2]), (self.m2[3], self.m2[4], self.m2[5]))
                    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    if len(cnts) > 0:
                        c = max(cnts, key = cv2.contourArea)
                        ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
                        if radius > 10:
                            thresh = cv2.inRange(image, (self.m3[0], self.m3[1], self.m3[2]), (self.m3[3], self.m3[4], self.m3[5]))
                            mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                            if len(cnts) > 0:
                                c = max(cnts, key = cv2.contourArea)
                                ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
                                if radius > 10:
                                    thresh = cv2.inRange(image, (self.m4[0], self.m4[1], self.m4[2]), (self.m4[3], self.m4[4], self.m4[5]))
                                    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                                    if len(cnts) > 0:
                                        c = max(cnts, key = cv2.contourArea)
                                        ((self.x, self.y), radius) = cv2.minEnclosingCircle(c)
                                        if radius > 10:
                                                image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
                                                cv2.imwrite("image.png", image)
                                                self.capture = False
                                                print("1 written!")
            ret, image = self.camera.read()
            if self.flip:
                image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def frame(self,*args):
        ret, image = self.camera.read()
        if self.flip:
            image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
        self.seq1, self.items1, self.flag1 = self.touch(image, self.seq1, self.seq2, self.m1, self.m2, self.items1, self.flag1)
        self.seq2, self.items2, self.flag2 = self.touch(image, self.seq2, self.seq1, self.m3, self.m4, self.items2, self.flag2)
        if self.capture:
            self.lock.acquire()
            try:  
                self.capture_pic(image) 
            finally:
                self.lock.release()

    def setCursorPos( self, pyp0,pyp1,yc0,yc1):
        yp=[0,0]
        if abs(yc0-pyp0)<5 and abs(yc1-pyp1)<5:
            yp[0] = yc0 + .7*(pyp0-yc0) 
            yp[1] = yc1 + .7*(pyp1-yc1)
        else:
            yp[0] = yc0 + .1*(pyp0-yc0)
            yp[1] = yc1 + .1*(pyp1-yc1)
        
        return yp[0],yp[1]

    def avgPoint(self,items):
        a,b=0,0
        for x,y in items:
            a=a+x
            b=b+y
        return a/len(items),b/len(items)
    def cam_loop(self):
        print('camera')
        self.serverSocket = socket.socket()
        port = 3335
        self.serverSocket.bind(('', port))  
        self.capture = False
        while True:
            self.serverSocket.listen(1)
            self.client, addr = self.serverSocket.accept()
            message = self.client.recv(1024).decode("ascii")
            self.capture = True
            time.sleep(2)
            self.lock.acquire()
            self.lock.release()
            f = open('image.png','rb') # Open in binary
            l = f.read(1024)
            while (l):
                self.client.send(l)
                l = f.read(1024)
            f.close()
            self.client.close()
                
            

    def main_thread(self):
        print ("main")
        while True:
            self.frame()

if __name__ == '__main__':
    a=cam(0,'192.168.43.8',3334,[117,49,472,268])
    t1 = threading.Thread(target=a.cam_loop)
    t2 = threading.Thread(target=a.main_thread)
    t1.start()
    t2.start()
    print("both started")
    
