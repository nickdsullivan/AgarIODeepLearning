#Author Nicholas Sullivan
#nickdsullivan@gmail.com

#This file describes the NN class
import numpy as np

import uuid 
import hickle as hkl 
import copy
class NN:
	#We will initialize the NN here.  
	#Takes the array sizes and interates through them making random weights of the size at the index
	def __init__(self,sizes,transType,transTypeOutput,id=None,learningRate=1e-2):
		#Keep track of which one is which for restarting
		if id ==None:
			self.id = uuid.uuid4()
		else:
			self.id = id

		#Stringify the file name once 
		self.fileName = "data/" + str(self.id) + "hkl"
		self.fileNameW = "data/W" + str(self.id) + ".csv"
		self.fileNameB = "data/B" + str(self.id) + ".csv"




		self.learningRate=learningRate
		self.width = len(sizes)
		self.weights= []
		self.biases = []
		self.trans_func = get_transition_func (transType)
		#TODO make it so multiple output funcs can happen.  
		self.outputFunc = get_transition_func (transTypeOutput)


		#init the first layer randomly
		size = sizes[0]
		layer = np.empty((size,size))
		for i in range(size):
				layer[i] = np.random.randn(size)
		self.weights.append(layer)
		self.biases.append(np.random.randn(size))

		#init the rest of the layers and biases
		for layerNumber in range(1,len(sizes),1):
			size = sizes[layerNumber]
			layer = np.empty((size,sizes[layerNumber-1]))
			for i in range(size):
				layer[i] = np.random.randn(sizes[layerNumber-1])

			self.weights.append(layer)
			self.biases.append(np.random.randn(size))




	def setLearningRate(learningRate):
		self.learningRate = learningRate
	#This is to replace the old NN no garbage needed!
	def replaceReplaceWeights(self,weights,biases):
		self.weights=weights
		self.biases=biases

	def slightRandomization(self):
		for layer in range(self.width):
			for unit in range(self.weights[layer].shape[0]):
				self.weights[layer][unit] = self.weights[layer][unit] + self.learningRate *np.random.randn(self.weights[layer][unit].shape[0])
				self.biases[layer][unit]= self.biases[layer][unit] + self.learningRate*np.random.randn(1)
	def returnSlightRandomization(self):
		weights = copy.deepcopy(self.weights)
		biases = copy.deepcopy(self.biases)
		for layer in range(self.width):
			for unit in range(self.weights[layer].shape[0]):
				weights[layer][unit] = self.weights[layer][unit] + self.learningRate *np.random.randn(self.weights[layer][unit].shape[0])
				biases[layer][unit]= self.biases[layer][unit] + self.learningRate*np.random.randn(1)
		return weights,biases
	def printWeights(self):
		print(self.weights)


	def printBiases(self):
		print(self.biases)
	#Saves weights and biases for next time
	def dumpData(self):
		hkl.dump([self.weights,self.biases],self.fileName)
	def getData(self):
		self.weights,self.biases = hkl.load(self.fileName)


	#This is the forward prop.  Pretty simple 
	def forward_pass(self,W,bs, X, trans_func,outputFunc):
		#W is a list of numpy arrays
		#X is a numpy array of inputs

		Z = X

		for i in range(len(W)-1):
			Z = np.matmul(W[i],Z) + bs[i]
			Z = trans_func(Z)
		Z = np.matmul(W[len(W)-1],Z) + bs[len(W)-1]
		return outputFunc(Z)

	def getOutput(self,X):
		return self.forward_pass(self.weights,self.biases,X,self.trans_func,self.outputFunc)

	#String to transition function
def get_transition_func(transType):
	if transType.lower() == 'sigmoid':
		trans_func = lambda z: 1 / (1+np.exp(-z))
	elif transType.lower() == 'relu2':
		trans_func = lambda z: 0.5 * (np.maximum(z, 0)**2)
	elif transType.lower() == 'tanh':
		trans_func = lambda z: np.tanh(z)
	elif transType.lower() == 'relu':
		trans_func = lambda z: np.maximum(z, 0)
	elif transType.lower() == 'zero-one':
		trans_func=lambda z: z>=0
	elif transType.lower() == 'linearzeroone':
		trans_func=lambda z:np.minimum(np.maximum(0,z), 1)
	else:
		raise ValueError('Unsupported transition function type: ' + transType) 

	return trans_func




