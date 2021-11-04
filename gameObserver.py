# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: theoo
"""

import camera
import sys
import imageWorker as iW
import cv2
import threading
import time #for debugging

class game(threading.Thread):
    
    
    #Init
    def __init__(self):
        threading.Thread.__init__(self)
        #Connect to camera
        self.cam = camera.camera()
        self.mov = ""






    def run(self):
        print("Started and waiting for instructions")
        # self.cam.cameraOn()  #Skrur på kameraet
        
        
        # #Create image worker
        # self.imgWork = iW.ImgWorker()  

        # im = self.cam.takeImage()    #take image
        
        # self.imgWork.addImg(iW.Image(im))  #add image to the worker
        
        self.debugMove()
        while True:
            pass
        

        
    
    def findMove(self):
    
        x,move = self.imgWork.getFromTo(-2,-1)
        cv2.imshow('after', x)  #For å vise hvor man beveget fra og til
        cv2.waitKey(0)
        return move      #retunerer move som ([x,y,farge,shape],[x,y,farge,shape])

    def fromTo(self, move):
        #Forsøker å finne ut hvilken rettning det flyttes
        #Forløpig har vi mest suksess med å se om senter er hvitt / svart
        if (move[0][2] == 'hvit' or move[0][2] == 'svart'): #hvis før ste x,y par har hvit/svart bakgrunn
            fro = move[0][0],move[0][1]     #så er det fra
            to = move[2][0],move[2][1]
        elif (move[2][2] == 'hvit' or move[2][2] == 'svart'):  #hvis ikke, omvendt
            fro = move[2][0],move[2][1]
            to = move[0][0],move[0][1]
        else: #det har under testing hendt at man ikke finner svart/hvit bakgrunn. 
        #farger for de andre brikkene er ikke lagt inn under riktige lysforholdene enda, men
        #man kan selvfølgelig benytte de
            fro ="error"
            to = "error"
        
            
        return fro,to
    
    def newPics(self): #Ta bilde og beregn bevegelse
        
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
       m = self.newPics()
       string = self.sendString(m)
       
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




