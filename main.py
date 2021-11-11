# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: buzzCraft
"""

import camera
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






def findMove4():

    x,move = imgWork.getFromTo(-2,-1)
    cv2.imshow('after', x)
    cv2.waitKey(0)
    return move

def fromTo(move):
    if (move[0][2] == 'hvit' or move[0][2] == 'svart'):
        fro = move[0][0],move[0][1]
        to = move[2][0],move[2][1]
    elif (move[2][2] == 'hvit' or move[2][2] == 'svart'):
        fro = move[2][0],move[2][1]
        to = move[0][0],move[0][1]
    else:
        fro ="error"
        to = "error"
        
    return fro,to

x=input("Waiting for user!: Press anykey")
im = cam.takeImage()   #take image
imgWork.addImg(iW.Image(im))
i = 0
x=""
while x != "q":
    cam.cameraOn()
    x=input("Waiting for user!: Press anykey")
    im = cam.takeImage()   #take image
    

    imgWork.addImg(iW.Image(im))
    cam.cameraOff()
    


    move = findMove4()
    mov = fromTo(move)
    print("from: " + str(mov[0]) + ", to: " +str(mov[1]))
    print(mov)

    # print("fra :" + str(fra))
    # print("til :" + str(til))
    # imgWork.getImg(-1).showImage()



# LIVE
cam.cameraOff()
