# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:17:47 2021

@author: theoo
"""

import threading
import cv2
import numpy as np
from skimage.metrics import structural_similarity



class ImgWorker(threading.Thread):

    def __init__(self):
        self.imageArray = []
        self.cleanArray = []
        self.boundaries = [ #BGR
       	([80, 70, 248], [10, 10, 170], ["orange"]),  #Orange
       	([45, 105, 90], [15, 70, 50], ["grønn"]),  #Grønn
       	([40, 110,160], [5, 65 ,100], ["gul"]), #Gul
       	([120,70,45], [50,35,15], ["blå"]), #lyse blå
        ([80,18,165], [48,5,118], ["rosa"]), #rosa
        ([15,10,120], [0,1,80], ["rød"]), #rød     
        ([130,125,155], [60,70,85], ["hvit"]), #hvit
        ([49,50,70], [0, 0, 0], ["svart"]) #svart
         ]

    #legger til et bilde i arrayet    
    def addImg(self, img):
        self.imageArray.append(img)
        self.cleanArray.append(img)
        
    #henter bilde fra bildearray    
    def getImg(self, index=-1):
        return self.imageArray[index]
    
    #skal trolig slettes
    def removeBackground(self, img = -1, th = 20):
        
        
        return self.getChange(0,img, th)
        
                
    #skal trolig slettes                
    def getChange(self, before = 0, after = -1, th = 20):
        img1 = self.imageArray[before].getOrig()
        img2 = self.imageArray[after].getImg()
        
        diff = cv2.absdiff(img1, img2)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        imask =  mask>th
        
        canvas = np.zeros_like(img2, np.uint8)
        canvas[imask] = img2[imask]
        return canvas
        
    def getColor(self, img, center=(50,50)):
        x = int(center[0])  #legger senter koordinater i x og y
        y = int(center[1])
        c1 = img[x, y]  #Finner farger på 5 steder rundt senter
        # print(c1)
        c2 = img[x+5, y]
        c3 = img[x-5, y]
        c4 = img[x, y+5]
        c5 = img[x, y-5]
        c = [0,0,0]  #Lager et tomt farge array
        
        for i in range(3):
            c[i]=int((int(c1[i])+int(c2[i])+int(c3[i])+int(c4[i])+int(c5[i]))/5)
            
        b = self.boundaries #legger boundaries i en egen var for å korte ned teksten
        color = "null"
        for i in range(len(self.boundaries)):  #Går igjennom hele listen med farger
            if (c[0] <= b[i][0][0] and c[0] >= b[i][1][0]): #Sjekker kanal for kanal
                if (c[1] <= b[i][0][1] and c[1] >= b[i][1][1]):
                    if (c[2] <= b[i][0][2] and c[2] >= b[i][1][2]):
                        color = b[i][2]  #Henter fargenavnet
        #retunerer fargen
        print(color)
        return color

        

        
        
        
    
    
    
    ########
    # Metoden vi trolig ender opp med å bruke
    ##########
    def getFromTo(self, pFrom = -2, pTo = -1):
        # before = self.removeBackground(pFrom)
        # after = self.removeBackground(pTo)
        before = self.imageArray[pFrom].getOrig()  #Henter blidet før flyttet
        after = self.imageArray[pTo].getImg()      #Henter bildet etter flytt
        after = np.ascontiguousarray(after, dtype=np.uint8)       #skalerer bildet om til en np.unit8 (for at det skal 
        #fungere greit seinere)
        black_bg = 0*np.ones_like(after)  #Lager en versjon hvor vi kan farge alt unntatt flyttet svart
        
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)  #Konverterer til grått
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)    #Konverterer til grått

        #Her må vi tune litt
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)  #Finner forskjellen
        cv2.imshow('after', diff)
        diff = (diff * 255).astype("uint8")   #Gjør noe jeg ikke helt skjønner med diff
        cv2.imshow('after', diff)
        cv2.waitKey(0)
        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        # thresh = cv2.threshold(diff,127,255,cv2.THRESH_BINARY_INV)[1]
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  #Finner en god threshold
        cv2.imshow('after', thresh)
        cv2.waitKey(0)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #Finner konturer
        contours = contours[0] if len(contours) == 2 else contours[1]      #Teller konturer
        
        # mask = np.zeros(before.shape, dtype='uint8')   #Lager en maske som legger seg over forskjellen i bildene
              
        filled_after = after.copy()        #Lager en kopi av bildet after
        cv2.drawContours(after, contours, -1, (0,255,0), 3)
        
        move = []
        for c in contours:   #Går igjennom alle konturene
        
            area = cv2.contourArea(c)  #Regner arealet
            # print(area)
            if area > 500:             #Hvis arealet er over 1000, (kan tunes litt)
                x,y,w,h = cv2.boundingRect(c)  #Finner en rektangel som passer over

                roi = filled_after[y:y + h, x:x + w]   #Kopierer ut kun endringen
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)  #Tegner på et rektangel for å visuellt se flyttet
                shape = self.findShape(roi, 10)
                print(shape)
                xc = int(x+w/2)   #Regner ut seneter i flyttet
                yc = int(y+h/2)
                
                #Sjekker for farge
                color = self.getColor(after, (yc,xc))

                # cv2.rectangle(after, (xc-2, yc-2), (xc+2, yc+2), (36,255,12), 2)  #tegner en liten rektangel i senter av flyttet
                
                #For debug
                # cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                # cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
                
                #Lager et bilde hvor alt utenom flyttet er svart
                black_bg[y:y+h, x:x+w] = roi
                
                #Tror dette skal bort, men tegner opp sener av flyttet
                cv2.rectangle(black_bg, (xc-2, yc-2), (xc+2, yc+2), (36,255,12), 2)
                move.append((xc,yc,color[0]))
                move.append(shape)
                # print(xc,yc)
                cv2.imshow('after', roi)
                cv2.waitKey(0)
                # self.getColor(black_bg,(xc,yc))
                

                
        
        #Retunerer et bilde med flyttet og 
        return after, move
    
        #Dektekterer shape og lager en liste med brikke, possisjon og farge (etterhvert)    
    def shape_helper(self, c, shapeW = 100):
        shape = ""
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # Square or rectangle
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
    
            # A square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            if w > shapeW:
                shape = "square"
    
        # Otherwise assume as circle or oval
        else:
            (x, y, w, h) = cv2.boundingRect(approx)

            if w > shapeW:
               shape = "circle" #if ar >= 0.95 and ar <= 1.05 else "oval"
    
        return shape
    
    #Finder en shape. Setter wSize for å si noe om hvor vid shapen minst skal være
    def findShape(self, image, wSize=100):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,7)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            shape = self.shape_helper(c, wSize)  #Finner shape
            if shape != "":
                return shape #Hvis vi har funnet en, supert
            else:
                shape = "No shape found" #Hvis ikke, return no shape
                return shape
               


# Klasse for hvert bilde
class Image():
    
    nr = 0  #Antall bilder i klassen
    
    def __init__(self, image, typ = 0, name=""):
        if (typ == 0):
            
            self.image = image
            self.OriginalImage = self.image.copy()
        else:    #Kun ved testing uten kamera
            self.image = cv2.imread(image)
            self.OriginalImage = self.image.copy()
        
        
        if name == "":  #Gir hvert bilde et navn
            self.name = str(Image.nr)
        else:
            self.name = name
        Image.nr += 1  #legg til en i antall bilder
        self.pieces = []
        
        
    def resetImg(self): #Setter bildet tilbake til orginal bilde
        self.image = self.OriginalImage.copy()
    #Return current image
    def getImg(self):
        return self.image
    
    #Return orignal image without edits
    def getOrig(self):
        return self.OriginalImage
    
    #Viser bildene
    def showImage(self):
        cv2.imshow(self.name, self.image)
        cv2.waitKey()
        
    def showImage2(self):
        cv2.imshow(self.name, self.image2)
        cv2.waitKey()
        
    def showOriginal(self):
        cv2.imshow(self.name, self.OriginalImage)
        cv2.waitKey()      

        
#Klasse som sikkert slettes hvis vi ikke velger å rydde brettet    
class Piece:
    def __init__(self, x,y,shape,color = None):
        self.x = x
        self.y = y
        if shape == "circle":
            self.white = True
        else:
            self.white = False
    
    def setPos(self, x,y):
        self.x = x
        self.y = y
    
    def getPos(self):
        return (self.x,self.y)
    
    def __str__(self):
        return f'X:{self.x} Y:{self.y} White: {self.white}'



if __name__ == "__main__":  
    imgWork = ImgWorker()    


        