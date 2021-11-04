# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: theoo
"""

import camera
import crop
import imageWorker as iW
import cv2

#LIVE
#Connect to camera
cam = camera.camera()
cam.cameraOn()


#Create image worker
imgWork = iW.ImgWorker()

im = cam.takeImage()    #take image

imgWork.addImg(iW.Image(im))  #add image to the worker




# def findMove2():
#     #Tar før - til
#     imgWork.getChange(-2,-1,80)
#     #Vi skal nå ha et bilde med to åpne "hull"
    
#     #Finner shpes og putter i fra
#     #Sjekker at vi kun har to endringer, øker eventuelt størrelsen på figur
#     fra = []
#     size = 40
#     while(len(fra)!=2):
#         fra = imgWork.getImg(-1).findShape(size)
#         size += 5
#         if (size == 150):
#             print("Can't find two changes")
#             break
#     imgWork.getImg(-1).showImage2()
#     imgWork.removeBackground(80)
#     size = 60
#     til = []
#     while(len(til)!=1):
#         til = imgWork.getImg(-1).findShape(size)
#         size += 5
#         if (size == 150):
#             print("Can't find one changes")
#             break
        
#     imgWork.getImg(-1).showImage2()
#     #resetter image 1, for å kunne sjekke igjen på neste
#     imgWork.getImg(-1).resetImg()
#     return (fra,til)





# #Funksjon som finner hvilken brikke som er flyttet mellom to bilder
# def findMove():

    
#     #PSUDO
#     # Ta vare på bakgrunn
#     # Ta første bilde - bakgrunn
#     # Ta andre bilde - første bilde
#     # Her får du fra - til
#     # Ta andre bilde - bakgrunn
#     # Her får du til

#     # imgWork.getChange(0,-1,50)
#     # imgWork.getChange(-1,-2,50)
#     imgWork.getChange(-1,-2,50)

#     #Trekk fra bakgrunn

#     fra = imgWork.getImg(-2).findShape(80) 
#     imgWork.getImg(-2).showImage2()
#     imgWork.removeBackground(70)
    


#     til = imgWork.getImg(-1).findShape(80)
#     imgWork.getImg(-1).showImage2()
#     # fra = [item for item in fra if item not in til]
#     imgWork.getImg(-1).resetImg()
#     return (fra,til)
# For fra, gjør det samme som til, men bare motsatt rekkefølge
def findMove3(th):
    #Tar før - til
    imgWork.getChange(-2,-1,th)
    #Vi skal nå ha et bilde med to åpne "hull"
    
    #Finner shpes og putter i fra
    #Sjekker at vi kun har to endringer, øker eventuelt størrelsen på figur

    # imgWork.getImg(-1).showImage2()
    imgWork.removeBackground(th)
    size = 10
    til = []
    imgWork.getImg(-1).blur(10,10)
    while(len(til)!=1):
        til = imgWork.getImg(-1).findShape(size)
        size += 5
        if (size == 150):
            print("Can't find to")
            break
        
    imgWork.getImg(-1).showImage2()
    imgWork.getChange(-1,-2,th)
    imgWork.getChange(0,-2,th)
    fra = []
    size = 40
    imgWork.getImg(-2).blur(10,10)
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

def findMove4():
    x = imgWork.getFromTo(-2,-1)
    cv2.imshow('after', x)
    cv2.waitKey(0)

x=input("Waiting for user!: Press anykey")
im = cam.takeImage()   #take image
imgWork.addImg(iW.Image(im))
i = 0
x=""
while x != "q":

    x=input("Waiting for user!: Press anykey")
    im = cam.takeImage()   #take image
    

    imgWork.addImg(iW.Image(im))


    findMove4()
    # print("fra :" + str(fra))
    # print("til :" + str(til))
    # imgWork.getImg(-1).showImage()



# LIVE
cam.cameraOff()

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