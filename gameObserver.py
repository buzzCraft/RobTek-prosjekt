# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: buzzCraft
"""

import camera
import sys
import imageWorker as iW
import cv2
# import threading
import time #for debugging

class game():
    
    
    #Init
    def __init__(self):
        # threading.Thread.__init__(self)
        #Connect to camera
        self.cam = camera.camera()
        self.mov = ""
        self.farger = ("orange", "grønn", "gul", "blå", "rosa", "rød")
        self.bakgrunn = ("hvit", "svart")
        
        #UNCOMMENT WHEN CONNECTED TO CAM
        self.cam.cameraOn()  #Skrur på kameraet
        #Create image worker
        self.imgWork = iW.ImgWorker() 
        im = self.cam.takeImage()    #take image
        
        self.imgWork.addImg(iW.Image(im))  #add image to the worker


        
    
    def findMove(self):
    
        x,move = self.imgWork.getFromTo(-2,-1)
        cv2.imshow('after', x)  #For å vise hvor man beveget fra og til
        cv2.waitKey(0)
        return move      #retunerer move som ([x,y,farge,shape],[x,y,farge,shape])

    def fromTo(self, move):
        #Forsøker å finne ut hvilken rettning det flyttes
        #Forløpig har vi mest suksess med å se om senter er hvitt / svart
        if (move[0][2] in self.bakgrunn): #hvis før ste x,y par har hvit/svart bakgrunn
            fro = move[0][0],move[0][1]     #så er det fra
            to = move[2][0],move[2][1]
        elif (move[2][2] in self.bakgrunn):  #hvis ikke, omvendt
            fro = move[2][0],move[2][1]
            to = move[0][0],move[0][1]
        elif(move[0][2] in self.farger): #hvis før ste x,y par har hvit/svart bakgrunn
            to = move[0][0],move[0][1]     #så er det fra
            fro = move[2][0],move[2][1]
        elif (move[2][2] in self.farger):  #hvis ikke, omvendt
            to = move[2][0],move[2][1]
            fro = move[0][0],move[0][1]
        
            
        return fro,to
    
    def newPicture(self): #Ta bilde og beregn bevegelse
        
        im = self.cam.takeImage()   #take image
        self.imgWork.addImg(iW.Image(im)) #legg bildet til i imageworker

        move = self.findMove()  #finn bevegelsen
        mov = self.fromTo(move) #beregn fra og til
        #Debug streng
        print("from: " + str(mov[0]) + ", to: " +str(mov[1]))
        #retuner movement
        return mov
    
    def sendString(self, mov):
        #Henter først ut alle movments
        x_from = str(mov[0][0])
        y_from = str(mov[0][1])
        x_to = str(mov[1][0])
        y_to = str(mov[1][1])
        
        #strengen som sendes skal ha en id: bxxxx (hvor hver x er lengden på nummeret som kommer)
        
        string = (f"b{len(x_from)}{len(x_to)}{len(y_from)}{len(y_to)};{x_from},{y_from},{x_to},{y_to}")
        return string
        
    def main_task(self):
        input("enter for debug")
        m = self.newPicture()
        string = self.sendString(m)
       #string = ("b3333;100,200,200,300") #string format
       # string = (6,0,5,0) #FOR DEBUG 
        print(string)
        return string
   
    
####Debugging##################   
    def debugMove(self):
        y  = self.delay()
        return y
    
    def delay(self):
        time.sleep(10)
        self.mov = 6,0
        time.sleep(1)
        self.mov = 5,0
        
    def getMov(self):
        return self.mov
    
    def setMov(self, mov):
        self.mov =mov
############################        
        
        
    def close(self):
        self.cam.cameraOff()
        sys.exit()




