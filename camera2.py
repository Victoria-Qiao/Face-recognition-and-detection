import threading
import numpy
from cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB, flip, imshow, waitKey
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class Camera(VideoCapture):

    

    
    def __init__(self, cameraNumber=None, cropWidth=None, cropHeight=None, showCropBox=True, flipImage=True):
        """A camera which can capture frame or show real-time image on QLabel. Inherits from cv2.VideoCapture"""

        super().__init__(cameraNumber)
        self.showCropBox = showCropBox
        self.flipImage = flipImage

        self.__cropWidth = 0
        self.__cropHeight = 0
        self.__cropXStart = 0
        self.__cropXEnd = 0
        self.__cropYStart = 0
        self.__cropYEnd = 0
        self.__cropBoxColor = [55, 137, 255]

        self.__displayThread = None
        self.__isDisplaying = False
        self.__qLabel = None

        self.setCropSize(cropWidth, cropHeight)
        
        

    def getCropSize(self):
        """Get the size of crop area in a tuple with format (width, height)"""
        return (self.__croself.setself.__cropHeight)
    

    def setCropSize(self, width=None, height=None):
        """Set the size of crop area on photo."""
        if not (width is None):
            self.__cropWidth = width
        if not (height is None):
            self.__cropHeight = height
        
        (isSuccess, frame) = self.read()
        if isSuccess:
            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            # Put the crop area at center of the whole frame
            self.__cropXStart = (frameWidth - self.__cropWidth) >> 1 # divide by 2 quickly
            self.__cropXEnd = self.__cropXStart + self.__cropWidth
            self.__cropYStart = (frameHeight - self.__cropHeight) >> 1 # divide by 2 quickly
            self.__cropYEnd = self.__cropYStart + self.__cropHeight
        

    def captureWhole(self):
        """Return a whole frame from camera in numpy matrix"""
        (isSuccess, frame) = self.read()
        if isSuccess:
            return cvtColor(frame, COLOR_BGR2RGB)
        #else:
        return None

    def captureCroped(self, cropWidth=None, cropHeight=None):
        """Obtain a frame from camera and crop it. Return the croped frame in numpy matrix"""
        if not ((cropWidth is None) and (cropHeight is None)):
            self.setCropSize(cropWidth, cropHeight)
        
        (isSuccess, frame) = self.read()
        if isSuccess:
            frame = cvtColor(frame, COLOR_BGR2RGB) #bgr to rgb
            # Crop the specified area in image matrix
            frame = frame[self.__cropYStart:self.__cropYEnd, self.__cropXStart:self.__cropXEnd]
            return numpy.copy(frame)
        #else:
        return None

        
    def setCropBoxColor(self, r, g, b):
        """ Set the color of crop box shown on QLabel real-time image"""
        self.__cropBoxColor[0] = r
        self.__cropBoxColor[1] = g
        self.__cropBoxColor[2] = b
        
    
    def startDisplayOnQLabel(self, qLabel):
        """Show real-time image from camera on a QLabel. This will be done on a new thread"""
        self.__qLabel = qLabel
        if not self.__isDisplaying:
            self.__isDisplaying = True
            if self.__displayThread is None:
                displayThread = threading.Thread(target=self.__displayOnQLable, daemon=True)
            displayThread.start()


    def __displayOnQLable(self):
        """Show real-time image from camera on a QLabel by continuely refresh"""
        while self.__isDisplaying:
            (isSuccess, frame) = self.read()

            if isSuccess:
                frame = cvtColor(frame, COLOR_BGR2RGB) #bgr to rgb
                # Draw crop box by set a range of pixel to specified color
                frame[self.__cropYStart, self.__cropXStart:self.__cropXEnd] = self.__cropBoxColor
                frame[self.__cropYEnd, self.__cropXStart:self.__cropXEnd] = self.__cropBoxColor
                frame[self.__cropYStart:self.__cropYEnd, self.__cropXStart] = self.__cropBoxColor
                frame[self.__cropYStart:self.__cropYEnd, self.__cropXEnd] = self.__cropBoxColor
                # Flip (mirror) the image
                if self.flipImage:
                    frame = flip(frame, 1)
                
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap(image)
                self.__qLabel.setPixmap(pixmap)
                
                    
    

    def stopDisplay(self):
        """Stop display"""
        if not (self.__displayThread is None):
            self.__isDisplaying = False
            while self.__displayThread.isAlive():
                pass
    

    def open(self, cameraNumber):
        """Open a camera"""
        super().open(cameraNumber)
        self.setCropSize()
    
    def release(self):
        """
        Release the connecting with a camera. Also kill the thread used to show real-time image on it \n
        The function should always be called if you want to close a camera, switch to another camera or stop the whole program
        """
        self.stopDisplay()
        super().release()
