# -*- coding: utf-8 -*-
"""
Tested 

Works
"""

import camera
import crop
import imageWorker as iW
import cv2
import math

def camCalib():
    # #LIVE
    # #Connect to camera
    cam = camera.camera()
    cam.cameraOn()
    
    
    #Create image worker
    imgWork = iW.ImgWorker()
    
    print("La bordet kun inneholde sjakkbrettet")
    input("Trykk enter når du er klar")
    im = cam.takeImage()    #take image
    imgWork.addImg(iW.Image(im))  #add image to the worker    

    
    print("Sett ut en brikke, tast inn x verdi og y verdi fra flexpedant")
    i1=input("x,y: ")
    
    i1 = tuple(float(x) for x in i1.split(","))
    
    im = cam.takeImage()    #take image
    imgWork.addImg(iW.Image(im))  #add image to the worker
    _, i1_p = imgWork.getFromTo() # _ er bildet som vi ikke trenger her
    print(i1_p)

    
    print("Sett ut en brikke til, tast inn x verdi og y verdi fra flexpedant")
    i2=input("x,y: ")
    
    i2 = tuple(float(x) for x in i2.split(","))
    
    im = cam.takeImage()    #take image
    imgWork.addImg(iW.Image(im))  #add image to the worker
    _,i2_p = imgWork.getFromTo()
    cam.cameraOff()
    P1=[i1[0],i1[1]]
    p1=[i1_p[0][0],i1_p[0][1]]
    P2=[i2[0],i2[1]]
    p2=[i2_p[0][0],i2_p[0][1]]
    
    print(P1)
    print(P2)
    print(p1)
    print(p2)
    
    y=math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    Y=math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2)
    
    
    mm = Y/y
    
    
    x0=P1[0]-p1[0]*mm
    y0=P1[1]-p1[1]*mm
    
    # print(x)
    

    return mm, p1

if __name__ == "__main__": 
    print(camCalib())


# P1[xxx,yyy]
# p1[rrr,uuu]
# mm = 0.3


