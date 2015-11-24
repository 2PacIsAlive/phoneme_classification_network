#!usr/bin/env python

from PIL import Image
import random
import glob
import math

class Neuron():
	def __init__(self):
		self.act = None
		self.inputConnections = []
		self.hiddenConnections = []
		self.outputConnections = []

class NeuralNetwork():
	def __init__(self):
		self.inputLayer = []
		self.hiddenLayer = []
		self.outputLayer = []
		self.inputActivations = []
		self.hiddenActivations = []
		self.outputActivations = []
		self.epochError = 0
		self.epochs = 0
		self.stateList = []

	def makeNetwork(self):
		for input_node in range(1000):
			self.inputLayer.append(Neuron())
		for hidden_node in range(5):
			self.hiddenLayer.append(Neuron())
		for output_node in range(2):
			self.outputLayer.append(Neuron())	

	def genInputActivations(self):
		for file_ in glob.glob("wavelets/*"):	
			phoneme = Image.open(file_)
			pix = list(phoneme.getdata())
			activation = []
			for pixel in pix:
				hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
				activation.append((int(hexval,16))/100000.0)
			self.inputActivations.append((activation,file_[9:-4]))

	def sigmoid(self,activation):
		return 1 / (1 + math.exp(-activation))
		
	def hiddenActivationFunction(self,node,index):
		f = 0
		for input_node in self.inputLayer:
			f += input_node.hiddenConnections[index][1] * float(input_node.act) 
		return self.sigmoid(f)

	def outputActivationFunction(self,node,index):
		f = 0
		for hidden_node in self.hiddenLayer:
			f += hidden_node.outputConnections[index][1] * float(hidden_node.act)
		#print "output:", f, "sigmoid:", self.sigmoid(f)
		return self.sigmoid(f)

	def getExpected(self,node,phoneme):
		if phoneme[1] == "a_f":
			if node == self.outputLayer[0]:
				expected = 1
			elif node == self.outputLayer[1]:
				expected = 0
		elif phoneme[1] == "a_m":
			if node == self.outputLayer[0]:
				expected = 0
			elif node == self.outputLayer[1]:
				expected = 1
		return expected

	def trainingEpoch(self):
		file_ = 0
		for phoneme in self.inputActivations:
			

			#FORWARD
			input_counter = 0
			for input_node in self.inputLayer:
				input_node.act = phoneme[0][input_counter]
				input_counter += 1
			hiddenConnection = 0 
			for hidden in self.hiddenLayer:
				hidden.act = self.hiddenActivationFunction(hidden,hiddenConnection)
				hiddenConnection += 1
			outputConnection = 0
			layerActivity = []
			for output in self.outputLayer:
				output.act = self.outputActivationFunction(output,outputConnection)
				layerActivity.append((output,output.act))
				outputConnection += 1
			#print layerActivity
			#print max(layerActivity, key = lambda x: x[1])
			choice = max(layerActivity, key = lambda x: x[1])
			#for node, act in layerActivity:
				#print "node: ", node, "act: ", act
			#layerActivity.remove(choice)
			if choice[0] == self.outputLayer[0]:
				phon = "a_f"
			elif choice[0] == self.outputLayer[1]:
				phon = "a_m"
			#print "Expected:", phoneme[1], "Output:", phon, "Node:", choice[0], "Activation:", choice[1]			
			#print "a_f unit activation: ",self.outputLayer[0].act
			#print "a_m unit activation: ",self.outputLayer[1].act
			correct = False
			if phoneme[1] == phon:
				correct = True			

			#BACKWARD
			outputCounter = 0
			for output in self.outputLayer:
				error = self.getExpected(output,phoneme) - output.act
				hiddenCounter = 0
				for hidden in self.hiddenLayer:
					new_weight = (hidden.act * 0.05 * error) + output.hiddenConnections[hiddenCounter][1]
					#print output, correct, "old: ", output.hiddenConnections[hiddenCounter][1], "new: ",new_weight
					output.hiddenConnections[hiddenCounter] = (hidden,new_weight)
					hidden.outputConnections[outputCounter] = (output,new_weight)
					inputCounter = 0
					for input_ in self.inputLayer:
						new_weight = (input_.act * 0.05 * error) + hidden.inputConnections[inputCounter][1]
						hidden.inputConnections[inputCounter] = (input_,new_weight)
						input_.hiddenConnections[hiddenCounter] = (hidden,new_weight)
						inputCounter += 1
					hiddenCounter += 1
				outputCounter += 1
			if correct == False:
				self.epochError += 1
				self.stateList.append(False)
			else:
				self.stateList.append(True)

	def initializeRandomWeights(self):
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				randomWeight = random.uniform(-1,1)
				input_node.hiddenConnections.append((hidden_node,randomWeight))
				hidden_node.inputConnections.append((input_node,randomWeight))
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				randomWeight = random.uniform(-1,1)
				hidden_node.outputConnections.append((output_node,randomWeight))
				output_node.hiddenConnections.append((hidden_node,randomWeight))

	def train(self):
		self.epochError = 0
		for i in range(100):
			self.trainingEpoch()
			self.epochs += 1
		if self.epochError < 1:
			return
		else:
			return self.train()

	def test(self):
		for activation, phoneme in self.inputActivations:
			print "Phoneme: ", phoneme[:-1]
			print "Gender: ", phoneme[-1:]

def main():
	net = NeuralNetwork()
	net.makeNetwork()
	net.initializeRandomWeights()
	net.genInputActivations()
	try:
		net.train()
		print "Error across 100 epochs: ", net.epochError
		print "Epochs to convergence:", net.epochs
		print net.stateList
	except RuntimeError:
		print "Training Failed"
	net.test()

if __name__=="__main__":
	main()
