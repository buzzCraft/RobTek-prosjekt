# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:17:47 2021

@author: buzzCraft
"""

# import threading
import cv2
import numpy as np
from skimage.metrics import structural_similarity



class ImgWorker():

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
        self.farger = ("orange", "grønn", "gul", "blå", "rosa", "rød")
        self.bakgrunn = ("hvit", "svart")

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

        c = [0,0,0]  #Lager et tomt farge array
        
        # for i in range(3):
        #     c[i]=int((int(c1[i])+int(c2[i])+int(c3[i])+int(c4[i])+int(c5[i]))/5)
        colArr = []
        for i in range(10):
            colArr.append(img[(x-5)+i,y])
            colArr.append(img[x,(y-5)+i])
        for i in range(3):
            for j in range(20):
                c[i] = c[i] + int(colArr[j][i])
            c[i] = c[i] / 20
            
        
        
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

        
    #Finner endringen mellom to bilder
    #Finner i pikselverdi hvor endringene har skjedd
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
        # cv2.imshow('after', diff)
        diff = (diff * 255).astype("uint8")   #Gjør noe jeg ikke helt skjønner med diff
        # cv2.imshow('after', diff)
        # cv2.waitKey(0)
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  #Finner en god threshold
        # cv2.imshow('after', thresh)
        # cv2.waitKey(0)
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #Finner konturer
        contours = contours[0] if len(contours) == 2 else contours[1]      #Teller konturer
        
        # mask = np.zeros(before.shape, dtype='uint8')   #Lager en maske som legger seg over forskjellen i bildene
              
        filled_after = after.copy()        #Lager en kopi av bildet after
        cv2.drawContours(after, contours, -1, (0,255,0), 3)
        
        move = []
        for c in contours:   #Går igjennom alle konturene
        
            area = cv2.contourArea(c)  #Regner arealet
            # print(area)
            if area > 1000:             #Hvis arealet er over 1000, (kan tunes litt)
                x,y,w,h = cv2.boundingRect(c)  #Finner en rektangel som passer over

                roi = filled_after[y:y + h, x:x + w]   #Kopierer ut kun endringen
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)  #Tegner på et rektangel for å visuellt se flyttet

                xc = int(x+w/2)   #Regner ut seneter i flyttet
                yc = int(y+h/2)
                
                #Sjekker for farge
                color = self.getColor(after, (yc,xc))
                shape = "none"
                if color[0] in self.farger:
                    
                    shape = self.findShape(filled_after, color[0], yc,xc, 25)
                    # print(shape)

                
                #Lager et bilde hvor alt utenom flyttet er svart
                black_bg[y:y+h, x:x+w] = roi
                
                #Tror dette skal bort, men tegner opp sener av flyttet
                cv2.rectangle(black_bg, (xc-2, yc-2), (xc+2, yc+2), (36,255,12), 2)
                move.append((xc,yc,color[0],shape))
                # move.append(shape)
                # print(xc,yc)
                cv2.imshow('after', after)
                cv2.waitKey(0)
                # self.getColor(black_bg,(xc,yc))
                

                
        
        #Retunerer et bilde med flyttet og 
        return after, move
    

            
    def findShape(self, img, color,x,y, pixJump=5):
        #img  bildet vi sjekker
        #color fargen til brikken
        #pixJump, hvor langt man hopper til en side for å se om det er sirkel eller firkant
        i=0
        
        pix = img[x+i,y] 

        while self.pixInColor(pix,color):
            i += 1
            pix = img[x+i,y]

        #Gå så en tilbake (i -=1 )
        #Hopp så pixJump i y og -y og se om vi finner fargen
        #Hvis en av de ja! -> Firkant
        #Hvis ingen -> Sirkel
        i -= 1

        p1 = img[x+i,(y+i-5)]
        p2 = img[x+i,(y-i+5)]

        if self.pixInColor(p1, color):
            shape = "firkant"
        elif self.pixInColor(p2, color):
            shape = "firkant"
        else:
            shape = "sirkel"
        print(shape)
        return shape
        
    def pixInColor(self, pix, color):
        for row in self.boundaries:
            if (row[2][0] == color):
                l = row[0]
                r = row[1]


        if pix[0]<=l[0] and pix[1]<=l[1] and pix[2]<=l[2] and pix[0]>=r[0] and pix[1]>=r[1] and pix[2]>=r[2]:
            return True
        else: return False
             


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

        




if __name__ == "__main__":  
    imgWork = ImgWorker()    


        