# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 12:51:14 2021

@author: buzzCraft
"""


import numpy as np
import cv2



from pyueye import ueye
from pyueye_camera import Camera
from pyueye_utils import ImageData, ImageBuffer  # FrameThread, 


#end try, import pyueye

#from appImageViewer1 import myPath, MainWindow as inheritedMainWindow 
# from myImageTools import np2qimage


class camera:
    
    def __init__(self):
        self.cam_on = False
        self.cam = None
        self.refrence = None
        self.imageArray = []
        self.npImage = np.array([])
        

    def cameraOn(self):
        """Turn IDS camera on."""
        if not self.cam_on:
            
            self.cam = Camera()
            self.cam.init()  # gives error when camera not connected
            self.cam.reset()
            self.cam.set_colormode(ueye.IS_CM_RGB8_PACKED)
            # self.cam.set_exposure_auto(0)
            self.cam.set_exposure(20)   #20
            #self.cam.set_gain_auto(0)
            self.cam.setGain(0,0,0,70)  #0,0,0,70
            # self.cam.setWhite(26, 5, 10)
            # This function is currently not supported by the camera models USB 3 uEye XC and XS.
            self.cam.set_aoi(528,118,852,850)  # AOI kan justeres
            self.cam.alloc(3)  # argument is number of buffers
            self.cam_on = True


            print(' cameraOn() Camera started ok' )
        #
        return
    
    def takeImage(self):
        """Get one image from IDS camera."""
        if self.cam_on:
            print('getOneImage() try to capture one image' )
            imBuf = ImageBuffer()  # used to get return pointers
            self.cam.freeze_video(True)
            retVal = ueye.is_WaitForNextImage(self.cam.handle(), 1000, imBuf.mem_ptr, imBuf.mem_id)
            if retVal == ueye.IS_SUCCESS:
                print('  ueye.IS_SUCCESS: image buffer id = %i' % imBuf.mem_id)
                self.imageArray.append(self.copy_image( ImageData(self.cam.handle(), imBuf) ))  # copy image_data 
                # self.showImage()
        return self.imageArray[-1]
    
    
    def setReference(self):
        self.getOneImage()                   #Ta et bilde
        self.refrence = self.imageArray[-1]  # Hent ut bilde og putt det som refrence
            
        return
    
    def getRefrence(self):
        return self.refrence
    
        
    def cameraOff(self):
        """Turn IDS camera off and print some information."""
        if self.cam_on:
            self.cam.exit()
            self.cam_on = False

            print('cameraOff() Camera stopped ok')
        return
    
    def showImage(self):
        cv2.imshow('thresssssh', self.imageArray[-1])
        cv2.waitKey(0)
    
    def copy_image(self, image_data):
        """Copy an image from camera memory to numpy image array 'self.npImage'."""
        tempBilde = image_data.as_1d_image()
        npImage = tempBilde
        
        if np.min(tempBilde) != np.max(tempBilde):
            npImage = np.copy(tempBilde[:,:,[2,1,0]])  # or [2,1,0] ??  RGB or BGR?
            print("copy_image(): 'self.npImage' is an ndarray of %s, shape %s." % (self.npImage.dtype.name, str(self.npImage.shape)))
        else:
            npImage = np.array([])  # size == 0
        #end if 
        image_data.unlock()  # important action
        return npImage
    
    def getImArray(self):
        return self.imageArray
    
    def getImage(self):
        if len(self.imageArray)>0:
            return self.imageArray[-1]
        else:
            print("Error: Non images taken!")
    
if __name__ == "__main__":       
    cam = camera()
    
    cam.cameraOn()
    cam.takeImage()
    cam.cameraOff()
    cam.showImage()
