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
        
        return move      #retunerer move som ([x,y,farge,shape],[x,y,farge,shape])

    def fromTo(self, move):
        #Forsøker å finne ut hvilken rettning det flyttes
        #Forløpig har vi mest suksess med å se om senter er hvitt / svart
        fro = [0,0]
        to = [0,0]
        if (move[0][2] in self.bakgrunn): #hvis før ste x,y par har hvit/svart bakgrunn
            fro = move[0][0],move[0][1]     #så er det fra
            to = move[1][0],move[1][1]
        elif (move[1][2] in self.bakgrunn):  #hvis ikke, omvendt
            fro = move[1][0],move[1][1]
            to = move[0][0],move[0][1]
        elif(move[0][2] in self.farger): #hvis før ste x,y par har hvit/svart bakgrunn
            to = move[0][0],move[0][1]     #så er det fra
            fro = move[1][0],move[1][1]
        elif (move[1][2] in self.farger):  #hvis ikke, omvendt
            to = move[1][0],move[1][1]
            fro = move[0][0],move[0][1]
        
            
        return fro,to
    
    def newPicture(self, pic): #Ta bilde og beregn bevegelse
        

        self.imgWork.addImg(iW.Image(pic)) #legg bildet til i imageworker

        move = self.findMove()  #finn bevegelsen

        print(f'{move[0][2]} {move[0][3]} flyttet fra {move[1][0]}, {move[1][1]} til {move[0][0]}, {move[0][1]} ')
        if len(move)==2: #Vanlig flytt

            mov = self.fromTo(move) #beregn fra og til
        elif len(move)==3: #enpasant
            print("Ikke implementert for hvit")
            mov = [0,0,7,6] #Feil bevegelse
        elif len(move)==4:
            #Sjekk om det er 2 svarte felter
            #Velg den med høyest verdi
            farger = [0,0,0,0] #svart, hvit, blå, grønn
            trekk =[] # en liste for å ta vare på to trekk
            for m in move:  #går igjennom alle bevegelser i move
                if (m[2] == "svart"): #Hvis vi har svart bakgrunn

                    farger[0] += 1    #Legg en til i svart
                    if (farger[0] < 1): #Hvis vi allerede har funnet en svart

                        for mov in trekk: #Sjekk lista med trekk for det svarte trekket
                            if (mov[2] == "svart"):
                                #Sjekk om det nye trekket er lengere til venstre
                                if abs(mov[0])+abs(mov[1]) > abs(m[0])+abs(m[1]): 
                                    mov[0] = m[0]  #Oppdaterer trekket hvis det nye er større
                                    mov[1] = m[1]

                                
                    else:  #Hvis første gang vi ser svart, legg til svart
                        trekk.append(m)

            
                elif (m[2] == "hvit"):
                    farger[1] += 1
                
                elif (m[2]=="blå"):
                    farger[2] += 1
                    trekk.append(m) #Legg til det blå trekket
                
                elif (m[2] == "grønn"):
                    farger[3] += 1
            mov = self.fromTo(trekk) #beregn fra og til

            if sum(farger) != 4:
                print("Error")
                mov = [0,0,7,6] #Feil bevegelse
            
            #Finn hvor blå står
            #Sender blå , svart(høyeste)
        else:
            print("Error")
            mov = [0,0,7,6] #Feil bevegelse 
        #Debug streng
        # print("from: " + str(mov[0]) + ", to: " +str(mov[1]))
  
        return mov
    
    def snapPicture(self):
        im = self.cam.takeImage()   #take image
        self.imgWork.addImg(iW.Image(im)) #legg bildet til i imageworker
        
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

        m = self.newPicture()
        string = self.sendString(m)

        return string
         
        
        
    def close(self):
        self.cam.cameraOff()
        sys.exit()




