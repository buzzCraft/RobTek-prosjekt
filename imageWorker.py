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
        
    def addImg(self, img):
        self.imageArray.append(img)
        self.cleanArray.append(img)
        
    def getImg(self, index=-1):
        return self.imageArray[index]
    
    def removeBackground(self, th = 20):
        
        self.getChange(0,-1, th)
        
                
                    
    def getChange(self, before = 0, after = -1, th = 20):
        img1 = self.imageArray[before].getOrig()
        img2 = self.imageArray[after].getImg()
        diff = cv2.absdiff(img1, img2)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        imask =  mask>th
        
        canvas = np.zeros_like(img2, np.uint8)
        canvas[imask] = img2[imask]
        self.imageArray[after].image = canvas
        
        
        
    def prosess(self, imgIndex):
        self.imageArray[imgIndex].blur(10,10)
        self.imageArray[imgIndex].getCnts()
        self.imageArray[imgIndex].assignPieces()
        #self.imageArray[imgIndex].showImage()
        
        return self.imageArray[imgIndex].getImg()
    
    
    ########
    # Metoden vi trolig ender opp med å bruke
    ##########
    def getFromTo(self, pFrom = -2, pTo = -1):
        before = self.imageArray[pFrom].getOrig()  #Henter blidet før flyttet
        after = self.imageArray[pTo].getImg()      #Henter bildet etter flytt
        after = np.ascontiguousarray(after, dtype=np.uint8)       #skalerer bildet om til en np.unit8 (for at det skal 
        #fungere greit seinere)
        black_bg = 0*np.ones_like(after)  #Lager en versjon hvor vi kan farge alt unntatt flyttet svart
        
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)  #Konverterer til grått
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)    #Konverterer til grått
        
        #Her må vi tune litt
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)  #Finner forskjellen
        
        diff = (diff * 255).astype("uint8")   #Gjør noe jeg ikke helt skjønner med diff
        
        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  #Finner en god threshold
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #Finner konturer
        contours = contours[0] if len(contours) == 2 else contours[1]      #Teller konturer
        
        # mask = np.zeros(before.shape, dtype='uint8')   #Lager en maske som legger seg over forskjellen i bildene
              
        filled_after = after.copy()        #Lager en kopi av bildet after
        
        
        
        for c in contours:   #Går igjennom alle konturene
            area = cv2.contourArea(c)  #Regner arealet
            if area > 1000:             #Hvis arealet er over 1000, (kan tunes litt)
                x,y,w,h = cv2.boundingRect(c)  #Finner en rektangel som passer over

                roi = filled_after[y:y + h, x:x + w]   #Kopierer ut kun endringen
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)  #Tegner på et rektangel for å visuellt se flyttet
                
                xc = int(x+w/2)   #Regner ut seneter i flyttet
                yc = int(y+h/2)
                cv2.rectangle(after, (xc-2, yc-2), (xc+2, yc+2), (36,255,12), 2)  #tegner en liten rektangel i senter av flyttet
                
                #For debug
                # cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                # cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
                
                #Lager et bilde hvor alt utenom flyttet er svart
                black_bg[y:y+h, x:x+w] = roi
                
                #Tror dette skal bort, men tegner opp sener av flyttet
                cv2.rectangle(black_bg, (xc-2, yc-2), (xc+2, yc+2), (36,255,12), 2)

                

                
        
        #Retunerer et bilde med flyttet
        return after



        

    
        
                        
            
           





class Image():
    
    nr = 0
    
    def __init__(self, image, typ = 0, name=""):
        if (typ == 0):
            
            self.image = image
            self.OriginalImage = self.image.copy()
        else:
            self.image = cv2.imread(image)
            self.OriginalImage = self.image.copy()
        
        
        if name == "":
            self.name = str(Image.nr)
        else:
            self.name = name
        Image.nr += 1
        self.pieces = []
        
        
    def scale(self, scale_percent = 60):
         # percent of original size
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

      
    # resize image
        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA) 
    
    def resetImg(self):
        self.image = self.OriginalImage.copy()
    #Return current image
    def getImg(self):
        return self.image
    
    #Return orignal image without edits
    def getOrig(self):
        return self.OriginalImage
    
    
    def showImage(self):
        cv2.imshow(self.name, self.image)
        cv2.waitKey()
        
    def showImage2(self):
        cv2.imshow(self.name, self.image2)
        cv2.waitKey()
        
    def showOriginal(self):
        cv2.imshow(self.name, self.OriginalImage)
        cv2.waitKey()
        
    def blur(self, image, x = 5, y = 5):
        return cv2.blur(image, (x, y))
        
        
        
    #Dektekterer shape og lager en liste med brikke, possisjon og farge (etterhvert)    
    def shape_helper(self, c, shapeW = 100):
        shape = ""
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)
        # Square or rectangle
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
    
            # A square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            if w > shapeW:
                shape = "square"
    
        # Otherwise assume as circle or oval
        else:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if w > shapeW:
               shape = "circle" #if ar >= 0.95 and ar <= 1.05 else "oval"
    
        return shape
    
    #Finder en shape. Setter wSize for å si noe om hvor vid shapen minst skal være
    def findShape(self, wSize=100):
        self.image2 = self.image.copy()
        gray = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)
        # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,7)
        thresh = self.blur(thresh, 100,100)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        
        pieces = []
        center = []

        for c in cnts:
            shape = self.shape_helper(c, wSize)
            if shape != "":
                x,y,w,h = cv2.boundingRect(c)
                xc=int((x+w/2)) #WTF er -5????
                yc=int(y+h/2)
                center.append((xc,yc))
                pieces.append(Piece(xc,yc,shape))
                cv2.putText(self.image2, ".", (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.putText(self.image2, shape, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.drawContours(image=self.image2, contours=c, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        return center
        
    

        
    
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

    def findMove():

        imgWork.getChange(-2,-1,20)
        imgWork.getImg(-1).showImage()
        fra = imgWork.getImg(-1).findShape() 
        
        #Trekk fra bakgrunn
        imgWork.getChange(0,-1,20)
    
        til = imgWork.getImg(-1).findShape()
        fra = [item for item in fra if item not in til]
        
        return (fra,til)

    def test():
        i1 = cv2.imread('./img/1.png')
        i2 = cv2.imread('./img/2.png')
        i3 = cv2.imread('./img/3.png')
        i4 = cv2.imread('./img/4.png')
        
        #Create imImgWorker()
        imgWork.addImg(Image(i1))
        imgWork.addImg(Image(i2))
        imgWork.addImg(Image(i3))
        fra,til= findMove()
        print("fra :" + str(fra))
        print("til :" + str(til))
        # imgWork.getImg(-1).showImage()
        
        imgWork.addImg(Image(i4))
        print("next")
        fra,til= findMove()
        print("fra :" + str(fra))
        print("til :" + str(til))
        imgWork.getImg(-1).showImage()
    
    def camTest():
        import camera
        #Connect to camera
        cam = camera.camera()
        cam.cameraOn()
        
        
        #Create image worker
        imgWork = ImgWorker()
        
        im = cam.takeImage()    #take image
        
        imgWork.addImg(Image(im))  #add image to the worker
        imgWork.getImg(-1).findShape(30)
        imgWork.getImg(-1).showImage2()
        input("Wait")
        im = cam.takeImage()    #take image  
        imgWork.addImg(Image(im))  #add image to the worker
        imgWork.removeBackground(70)
        imgWork.getImg(-1).findShape(30)
        imgWork.getImg(-1).showImage2()
        cam.cameraOff()
    camTest()
        