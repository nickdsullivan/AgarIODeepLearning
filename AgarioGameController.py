#Author Nicholas Sullivan
#nickdsullivan@gmail.com


#This file defines the class Game.  
#Game 
import numpy as np


import pyautogui
import cv2

class AgarioGameController:
	#initializes the game
	def __init__(self,browser,size=(800,800)):
		self.browser = browser
		self.size = size
		self.params=self.setBlobParamsByInFileValue()

	#get the current image 
	def getImage(self,border=20):
		self.browser.save_screenshot("images/image.png")
		image = cv2.bitwise_not(cv2.imread("images/image.png", cv2.IMREAD_GRAYSCALE))
		image = cv2.copyMakeBorder(image, border, border, border, border, borderType=cv2.BORDER_CONSTANT,value=(512, 521, 3))
		return image



	#Edit the values here if you want to get a certain the parameter for the image recongition
    #You can also do this in main just might be easier to do it here

	def setBlobParamsByInFileValue(self):	
		self.params = cv2.SimpleBlobDetector_Params()
		self.params.filterByCircularity = False
		self.params.minCircularity = .4
		self.params.maxCircularity = 1
		self.params.minDistBetweenBlobs = 0.0001
		self.params.filterByArea = False
		self.params.minArea = 1
		self.params.maxArea = 500000
		self.params.filterByInertia = False
		self.params.minInertiaRatio = .00001
		self.params.maxInertiaRatio = 1
		self.params.filterByConvexity = False
		self.params.minConvexity = .5
		self.params.maxConvexity = 1
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
		self.params.minConvexity = .5
		self.params.maxConvexity = 1

		return self.params



	#From an image find the blobs and return them/make a pretty picture
	def getBlobs(self,image,displayImage = False):
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
		if not self.isInTextRegion(blob):
		    blobs.append(blob)
		if displayImage:
			image = cv2.drawKeypoints(image, found_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			cv2.imshow("Keypoints", image)
			cv2.waitKey(0)
		return blobs
	def isInTextRegion(self,blob):
		x, y = blob.getCoords()
		if .9 * self.size[1] <= y <= self.size[1] and 0 <= x <= .22 * self.size[0]:
			return True
		else:
			return False

class Blob:
	def __init__(self,x,y,radius):
		self.x = x
		self.y = y
		self.radius = radius
	def getCoords(self):
		return self.x,self.y
	def getSize(self):
		return radius











