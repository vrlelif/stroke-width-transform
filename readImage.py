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

    def get_edges_Otsu(im):
        blur = cv2.GaussianBlur(im,(5,5),0)
        th,otsuResult = cv2.threshold(blur,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        edges = cv2.Canny(otsuResult, th, 255, 5)
        return edges
        
        
    def getGradientDirections(image): #get gradient directions
        gradientX = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1,dy=0, ksize=-1) #get x gradient
        gradientY = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0,dy=1, ksize=-1) #get y gradient
        return np.arctan2(gradientY, gradientX) # get gradient directions and return an image

    def initialize_SW_Map(edgeImage):
        SW_Map = np.matrix(np.ones(edgeImage.shape) * np.inf)
        return SW_Map

    
