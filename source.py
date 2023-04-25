import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time as t
import random

cap=cv.VideoCapture(0)
detector=HandDetector()

class Ashmap():
    
    def __init__(self):
        self.timer = 0
        self.stateResult = False  
        self.startGame = False
        self.score=[0,0]
        self.startGameFun()
        
    def startGameFun(self):

        while True:
            imgBk = cv.imread("mainimg.png")
            success,img = cap.read()
   
            imgScaled = cv.resize(img,(0,0),None,0.875,0.730)
            imgScaled=imgScaled[:,8:311]
            imgBk[235:585,633:936]=imgScaled
    
            self.hands ,self.img=detector.findHands(imgBk)
            if self.startGame:
                if self.stateResult is False:
                    timer=t.time()-self.initialTime
                    cv.putText(imgBk,str(int(timer)),(472,418),cv.FONT_HERSHEY_PLAIN,5,(255,255,255),4)
                    if timer>3:
                        self.stateResult = True
                        timer=0 
                        if self.hands:
                            self.findFingersCount()
                           
                           
            if self.stateResult:
                self.img = cvzone.overlayPNG(self.img,self.imgAI,(130,310))
            else:
                self.robot=cv.imread("robot.png",cv.IMREAD_UNCHANGED)
                self.img = cvzone.overlayPNG(self.img,self.robot,(105,300))
        
   
            cv.putText(self.img,str(int(self.score[0])),(315,220),cv.FONT_HERSHEY_PLAIN,3,(255,255,255),4)
            cv.putText(self.img,str(int(self.score[1])),(885,220),cv.FONT_HERSHEY_PLAIN,3,(255,255,255),4)
            cv.imshow("RPS Battle",self.img)
   
            key= cv.waitKey(1)
            if  key== ord('q'):
                break 
            if key==ord('s'):
                self.startGame = True
                self.initialTime =t.time()
                self.stateResult = False
                
    def findFingersCount(self):
       
        self.hand=self.hands[0]
        fingers=detector.fingersUp(self.hand)
        playerMove=1
        if fingers == [0,0,0,0,0]:
            playerMove=1
        if fingers ==[1,1,1,1,1]:
            playerMove=2
        if fingers == [0,1,1,0,0]:
            playerMove=3
        
        ran = random.randint(1,3)
        listimg=['2.png','1.png','3.png']
        self.imgAI=cv.imread(listimg[ran-1],cv.IMREAD_UNCHANGED)
        self.img = cvzone.overlayPNG(self.img,self.imgAI,(130,310))      
        
         
        if (playerMove ==1 and ran==3) or (playerMove==2 and ran==1) or (playerMove==3 and ran==2):
            self.score[1]+=1
                            
        if (playerMove==1 and ran==2) or (playerMove==2 and ran==3) or (playerMove==3 and ran==1):
            self.score[0]+=1
        
Ashmap()
