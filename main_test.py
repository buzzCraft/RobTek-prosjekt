# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: theoo
"""

import camera
import crop
import imageWorker as iW
import cv2

# #LIVE
# #Connect to camera
# cam = camera.camera()
# cam.cameraOn()

### TESTING
i1 = cv2.imread('./img/t/bg.bmp')
i2 = cv2.imread('./img/t/1.bmp')
i3 = cv2.imread('./img/t/2.bmp')
i4 = cv2.imread('./img/t/3.bmp')
i5 = cv2.imread('./img/t/4.bmp')
i6 = cv2.imread('./img/t/5.bmp')
i7 = cv2.imread('./img/t/6.bmp')

#Create image worker
imgWork = iW.ImgWorker()

# # LIVE
# #Take image, add it to the image worker
# im = cam.takeImage()    #take image
# #x,y,w,h=crop.crop(im)     #find the board 
# #im = im[y:y+h, x:x+w]  #crop the image
# imgWork.addImg(iW.Image(im))  #add image to the worker

### TESTING
imgWork.addImg(iW.Image(i1))

def findMove2():
    #Tar før - til
    imgWork.getChange(-2,-1,80)
    #Vi skal nå ha et bilde med to åpne "hull"
    
    #Finner shpes og putter i fra
    #Sjekker at vi kun har to endringer, øker eventuelt størrelsen på figur
    fra = []
    size = 40
    while(len(fra)!=2):
        fra = imgWork.getImg(-1).findShape(size)
        size += 5
        if (size == 150):
            print("Can't find two changes")
            break
    imgWork.getImg(-1).showImage2()
    imgWork.removeBackground(80)
    size = 60
    til = []
    while(len(til)!=1):
        til = imgWork.getImg(-1).findShape(size)
        size += 5
        if (size == 150):
            print("Can't find one changes")
            break
        
    imgWork.getImg(-1).showImage2()
    #resetter image 1, for å kunne sjekke igjen på neste
    imgWork.getImg(-1).resetImg()
    return (fra,til)


# For fra, gjør det samme som til, men bare motsatt rekkefølge
def findMove3():
    #Tar før - til
    imgWork.getChange(-2,-1,80)
    #Vi skal nå ha et bilde med to åpne "hull"
    
    #Finner shpes og putter i fra
    #Sjekker at vi kun har to endringer, øker eventuelt størrelsen på figur

    # imgWork.getImg(-1).showImage2()
    imgWork.removeBackground(80)
    size = 60
    til = []
    while(len(til)!=1):
        til = imgWork.getImg(-1).findShape(size)
        size += 5
        if (size == 150):
            print("Can't find to")
            break
        
    
    imgWork.getImg(-2).showImage()
    imgWork.getImg(-2).showImage()
    imgWork.getImg(-1).showImage2()
    imgWork.getChange(-1,-2,80)
    imgWork.getChange(0,-2,80)
    fra = []
    size = 40
    while(len(fra)!=1):
        fra = imgWork.getImg(-2).findShape(size)
        size += 5
        if (size == 150):
            print("Can't find from")
            break

    imgWork.getImg(-2).showImage2()
    #resetter image 1, for å kunne sjekke igjen på neste
    imgWork.getImg(-1).resetImg()
    return (fra,til)



#Funksjon som finner hvilken brikke som er flyttet mellom to bilder
def findMove():

    imgWork.getChange(-2,-1,20)
    imgWork.getImg(-1).showImage()
    fra = imgWork.getImg(-1).findShape() 
    
    #Trekk fra bakgrunn
    imgWork.getChange(0,-1,20)

    til = imgWork.getImg(-1).findShape()
    fra = [item for item in fra if item not in til]
    
    return (fra,til)

imgWork.addImg(iW.Image(i1))
l = [i2,i3,i4,i5,i6]
c = 0
x=""
while c != 5:

    x=input("Waiting for user!: Press anykey")
    #im = cam.takeImage()   #take image

    imgWork.addImg(iW.Image(l[c]))

    fra,til = findMove3()
    print("fra :" + str(fra))
    print("til :" + str(til))
    c+=1
    # imgWork.getImg(-1).showImage()



# # LIVE
# cam.cameraOff()

#TODO- 
# Siden vi skalerer så må vi ta vare på x,y, vi skalerer fra
#     disse verdiene benyttes senere til å finne robotverden verdier


#TODO-
# Første bilde som Base
# Andre bilde med brikker
# Tredje bilde, flytter en brikke
#     Finn først endring fra andre til første bilde
#         Ta vare på begge objekters x og y
#     Finn så endring fra tredje og første bilde
#         Finn hvilken x / y som har forsvunnet
#         Den som har forsvunnet er "fra", den som er igjen er "til"

#TODO
# Ta bilde av brettet
# Finn alle brikker
#     Gi alle en id basert på form og farge
#     Send id og plassering til Rapid