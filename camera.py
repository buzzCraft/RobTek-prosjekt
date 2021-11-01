_appFileName = "appImageViewer2"
_author = "Karl Skretting, UiS" 
_version = "2020.11.11"

import sys
import os.path
import numpy as np
import cv2
import ctypes

# try:
#     from PyQt5.QtCore import Qt, QPoint, QRectF, QT_VERSION_STR
#     from PyQt5.QtGui import QImage, QPixmap, QTransform
#     from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QFileDialog, QLabel, 
#             QGraphicsScene, QGraphicsPixmapItem)
# except ImportError:
#     raise ImportError("%s: Requires PyQt5." % _appFileName)
# #end try, import PyQt5 classes


from pyueye import ueye
from pyueye_example_camera import Camera
from pyueye_example_utils import ImageData, ImageBuffer  # FrameThread, 


#end try, import pyueye

#from appImageViewer1 import myPath, MainWindow as inheritedMainWindow 
from myImageTools import np2qimage


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
            self.cam.setGain(0,0,0,50)
            self.cam.setWhite(26, 5, 10)
            # This function is currently not supported by the camera models USB 3 uEye XC and XS.
           # self.cam.set_aoi(0, 0, 720, 1280)  # but this is the size used
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
