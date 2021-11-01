# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:17:47 2021

@author: theoo
"""

import threading
import cv2
import numpy as np



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
    
    def getFromTo(self, pFrom = -2, pTo = -1):
        # picFrom = self.imageArray[pFrom].image
        # picTo = self.imageArray[pTo].image
        
        #Finds change between two pics
        self.getChange(pFrom,pTo,20)
        
        
        #Get coordinate change
        coord_from = self.imageArray[pTo].assignPieces()
        #Remove background
        self.removeBackground(20)
        #Get remaining coordinate
        
        coord_to = self.imageArray[pTo].image.assignPieces()
        #Remove the coordinate in from list that is in the to list
        coord_from = [item for item in coord_from if item not in coord_to]
        #Repacage the coordinates
        x = [coord_from, coord_to]
        #Tup  FROM    TO
        tup=x[0][0],x[1][0]
        return tup
        
#             image1,til = shaping(image1)    
        # first,p2 = shaping(first)
        # #cv2.imshow('thresh', thresh)
        # cv2.imshow('image', image1)
        
        # cv2.imshow('image', first)
        
        # print(p2)
        
        
                        
            
           





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
        
    def blur(self, x = 5, y = 5):
        self.image = cv2.blur(self.image, (x, y))
        
        
        
    #Dektekterer shape og lager en liste med brikke, possisjon og farge (etterhvert)    
    def shape_helper(self, c, shapeW = 100):
        shape = ""
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
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
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.adaptiveThreshold(sharpen,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,7)
        
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
        imgWork.getImg(-1).findShape(50)
        imgWork.getImg(-1).showImage2()
        input("Wait")
        im = cam.takeImage()    #take image  
        imgWork.addImg(Image(im))  #add image to the worker
        imgWork.removeBackground(35)
        imgWork.getImg(-1).findShape(30)
        imgWork.getImg(-1).showImage2()
        cam.cameraOff()
    camTest()
        