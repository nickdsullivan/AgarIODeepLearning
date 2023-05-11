#Author Nicholas Sullivan
#nickdsullivan@gmail.com


#This controls the main game
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import time
import os.path
import cv2
import browserFunctions as bf
from AgarioGameController import AgarioGameController
from ai import NN
import time
import pickle as pickle
import random
######################################
# CONSTANTS

## Size sets the size of the window  
window_size = (800,800)



#Number of blobs that will be relavent to the NN
blobs_inputed = 10

######################################

######### AD BLOCK STUFF. UNCOMMENT IF YOU HAVE DONE THIS STUFF #########
chrome_options = Options()
#I think this will work but I am not sure
file = 'gighmmpiobklfepjocnamgkkbiglidom/5.6.0_0.crx'
chrome_options.add_extension(file);
######################################


game = AgarioGameController(None)
img = cv2.imread('images/aimg3.png',cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (0,0), fx=.2,fy=.2)
img = game.addBorderToImage(img)
blobs = game.getBlobs(img,displayImage=False)
blobs = sorted(blobs, key=lambda blob: (-1*blob.radius))

blobs = blobs[0:blobs_inputed]
X = np.array(game.blobsToX(blobs)).T




sizes = [2,3,1]
#model = NN(sizes,'relu','linearZeroOne',id=1)

XTrain = [[0,0],[0,1],[1,0],[1,1]]
YTrue = [0,1,1,0]
models = []




def make_models(numModels):
	for i in range(100):
		models.append(NN(sizes,'relu','zero-one',id=1,learningRate=1e-1))


def error(Ys,YTrues):
	error = 0
	for i in range(len(Ys)):
		if Ys[i] != YTrues[i]:
			error = error +1

	return error/len(Ys)
def getModelSplit(errors,percentage):
	sortedModels=dict(sorted(errors.items(),key= lambda x:x[1]))
	return list(sortedModels.keys())[0:int(len(sortedModels.items())*percentage)],list(sortedModels.keys())[int(len(sortedModels.items())*percentage):]





#This is the main game loop
count = 0
stopping_Flag = True

while stopping_Flag:
	#This is for debugging
	if count > 1000:
		stopping_Flag = False


	#Increase debugging var
	count = count + 1


	deaths = [False*len(models)]

	#This will store our errors
	scores = {}

	#Get the output
	for index in range(len(models)):

		while not deaths[index]:
			try:
				yPred = []
				#here we get the current screen
				image = game.getImage()
				image = cv2.resize(img, (0,0), fx=.2,fy=.2)
				#we then get the score 
				score = game.getScore(image)
				#More image processing
				image = game.addBorderToImage()
				#Finally have the inputs
				blobs = game.getBlobs(image)
				#choose the biggest blobs to input
				blobs = sorted(blobs, key=lambda blob: (-1*blob.radius))
				blobs = blobs[0:blobs_inputed]
				#Turn them int
				inputs = game.blobsToX(blobs)
				Y = models[index].getOutput()
				#finally actuall
				game.YtoAction(Y)
			except:
				if bf.checkForPlayButton(browser):
					print("Died.  Score: " + str(score))
					scores[models[index]] = score
					deaths[index] = True
					bf.startAgarioGame(browser,timeBetweenTries=2,timeAfterClickingPlay=2,restart = True)
				else:
					print("No score and no playbutton.  Something might be wrong")
					continue


		errors[model] = (error(yPred,YTrue))
	errornp = np.array(list(errors.values()))

	print("Min " + str(min(errornp)))
	print("Mean " + str(errornp.mean()))
	goodModels,badModels = getModelSplit(errors,.2)

	for model in badModels:
		if random.random()>.5:
			good_model_chosen_index = int(random.random()*len(goodModels))
			good_model = goodModels[good_model_chosen_index]
			w,b = good_model.returnSlightRandomization()
			model.replaceReplaceWeights(w,b)




#print(model.getOutput(X))
#model.printBiases()
#model.slightRandomization()
#model.printBiases()
'''

#First get the selinium browser object

browser = bf.initBrowser(window_size, options=chrome_options)
bf.openPage(browser=browser,webpage='http://agar.io')
bf.startAgarioGame(browser,timeAfterClickingPlay=2)
game = AgarioGameController(browser)




#This will keep track of how many times we have tried to do something that should be done if the game was playing
#If it reaches the threshold then we think the game is over



#current testing game loop
score = 0
while True:
	#img = cv2.imread('images/image.png',cv2.IMREAD_GRAYSCALE)
	img = game.getImage()
	try:
		score = game.getScore(img)
		needResetCounter = 0
	except:
		if bf.checkForPlayButton(browser):

			print("Died.  Score:" + str(score))
			bf.startAgarioGame(browser,timeBetweenTries=2,timeAfterClickingPlay=2,restart = True)
		else:
			print("No score and no playbutton.  Something might be wrong")
		continue


'''

