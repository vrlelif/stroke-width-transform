import cv2 
import numpy as np

class Read:
    def getImage(path):  # get image and read it as RGB
        image = cv2.imread(path)
        return image

    def getImageAsGrayScale(path):  # get image and read it as grayscale
        image = cv2.imread(path, 0)
        return image

    def get_edges(im, lo: float = 200, hi: float = 300, window: int = 3):
        edges = cv2.Canny(im, lo, hi, apertureSize=window)
        return edges
        
    def getGradientDirections(image): #get gradient directions
        gradientX = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1,dy=0, ksize=-1) #get x gradient
        gradientY = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0,dy=1, ksize=-1) #get y gradient
        return np.arctan2(gradientY, gradientX) # get gradient directions and return an image

    def initialize_SW_Map(edgeImage):
        SW_Map = np.matrix(np.ones(edgeImage.shape) * np.inf)
        return SW_Map

    
