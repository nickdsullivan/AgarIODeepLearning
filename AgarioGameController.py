#Author Nicholas Sullivan
#nickdsullivan@gmail.com


#This file defines the class Game.  
#Game 
import numpy as np

from PIL import Image
from pytesseract import pytesseract
import math
import pyautogui
import cv2

class AgarioGameController:

	#initializes the game
	def __init__(self,browser,size=(800,800)):
		self.browser = browser
		self.size = size
		self.params=self.setBlobParamsByInFileValue()

	#get the current image 
	def getImage(self):
		self.browser.save_screenshot("images/image.png")
		image = cv2.imread("images/image.png", cv2.IMREAD_GRAYSCALE)
		return image

	#this returns the score from an image
	def getScore(self,image):
		#Formula to find the score assuming it scales evenly with size.  
		#We know for 800,800 window size it should be (1350:1370, 20:120)
		yStart = int((self.size[1])/(800/1350))
		yEnd = int((self.size[1])/(800/1370))
		xStart = int((self.size[0])/(800/20))
		xEnd = int((self.size[0])/(800/120))
		crop = image[yStart:yEnd, xStart:xEnd] 

		#Here we get the raw text
		text = pytesseract.image_to_string(crop)

		x = np.array(text.split())
		res = x[np.char.isnumeric(x)].astype(int)
		return(int(res))

	#This adds a border to the image for more feature engineering
	def addBorderToImage(self,image,border=20):
		return cv2.copyMakeBorder(image, border, border, border, border, borderType=cv2.BORDER_CONSTANT,value=(0, 0, 0))


	#Edit the values here if you want to get a certain the parameter for the image recongition
    #You can also do this in main just might be easier to do it here

	def setBlobParamsByInFileValue(self):	
		self.params = cv2.SimpleBlobDetector_Params()
		self.params.filterByCircularity = True
		self.params.minCircularity = .0001
		self.params.maxCircularity = 1
		self.params.minDistBetweenBlobs = 0.000001
		self.params.filterByArea = True
		self.params.minArea = 1
		self.params.maxArea = 5000000
		self.params.filterByInertia = True
		self.params.minInertiaRatio = .0001
		self.params.maxInertiaRatio = 1
		self.params.filterByConvexity = True
		self.params.minConvexity = .001
		self.params.maxConvexity = 100
		self.params.minThreshold = 30
		self.params.maxThreshold = 100000
		return self.params
   	#Sets the values for the parameters
	def setBlobParamsByValue(self,filterByCircularity=False,minCircularity=.0001,maxCircularity=1,minDistBetweenBlobs=.0001,filterByArea=False,minArea=1,maxArea=1000,filterByInertia=False,minInertiaRatio=.0001,maxInertiaRatio=1,filterByConvexity = False,minConvexity=.0001,maxConvexity =1):
		self.params = cv2.SimpleBlobDetector_Params()
		self.params.filterByCircularity = filterByCircularity
		self.params.minCircularity = minCircularity
		self.params.maxCircularity = maxCircularity
		self.params.minDistBetweenBlobs = minDistBetweenBlobs
		self.params.filterByArea = filterByArea
		self.params.minArea = minArea
		self.params.maxArea = maxArea
		self.params.filterByInertia = filterByInertia
		self.params.minInertiaRatio = minInertiaRatio
		self.params.maxInertiaRatio = maxInertiaRatio
		self.params.filterByConvexity = filterByConvexity
		self.params.minConvexity = minConvexity
		self.params.maxConvexity = maxConvexity

		return self.params


	def getBlobs(self,image,displayImage=False):
		#Blur the image 
		img_blur = cv2.GaussianBlur(image,(3,3), sigmaX=0, sigmaY=0) 
		#img_blur = cv2.GaussianBlur(img_blur,(3,3), sigmaX=0, sigmaY=0) 
		edges = cv2.Canny(image=img_blur, threshold1=200, threshold2=100) 
		
		if displayImage:		
			cv2.imshow('Edges Graph', edges)
			cv2.waitKey(0)
		#newImage = (sobelxy/256).astype('uint8')
		return self.getBlobsInternal(edges,displayImage)


	#From an image find the blobs and return them/make a pretty picture
	def getBlobsInternal(self,image,displayImage = False):
		#Unclear what this does at the moment
		center_x = self.size[0]/2
		center_y = self.size[1]/2

		#cv2 version stuff
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3:
			detector = cv2.SimpleBlobDetector(self.params)
		else: 
			detector = cv2.SimpleBlobDetector_create(self.params)
		
		#detect the blobs
		found_blobs = detector.detect(image) 
		#list of the blobs
		blobs = []
		#Go through each blob and create a blob object for it
		for blob in found_blobs:
			blob = Blob(blob.pt[0]-20, blob.pt[1]-20, blob.size/2)
			blobs.append(blob)
		if displayImage:
			image_keypoints = cv2.drawKeypoints(image, found_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			cv2.imshow("Keypoints", image_keypoints)
			cv2.waitKey(0)
		return blobs
	def blobsToX(self,blobs):
		output = []
		for blob in blobs:
			x = blob.getCoords()[0]
			y = blob.getCoords()[1]
			size = blob.getSize()
			output.append(x)
			output.append(y)
			output.append(size)
		return output
	def YtoAction(self,Y):
		#From our 
		x = math.cos(2*3.14 * Y[0])
		y = math.sin(2*3.14 * Y[0])
		pyautogui.moveTo(x, Y)
		pyautogui.press('w')

class Blob:
	def __init__(self,x,y,radius):
		self.x = x
		self.y = y
		self.radius = radius
	def __str__(self):
		return "Location: " + str(self.getCoords()) + " Size: " + str(self.getSize())
	def getCoords(self):
		return self.x,self.y
	def getSize(self):
		return self.radius










