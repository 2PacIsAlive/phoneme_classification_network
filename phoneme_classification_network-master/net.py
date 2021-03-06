#!usr/bin/env python

from PIL import Image
#from gtts import gTTS
import random
import glob
import math
import os
import subprocess

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
		for hidden_node in range(8):
			self.hiddenLayer.append(Neuron())
		for output_node in range(4):
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

	def getPhoneme(self,node):
		if node == self.outputLayer[0]:
			return "a_f"
		elif node == self.outputLayer[1]:
			return "a_m"
		elif node == self.outputLayer[2]:
			return "chi_f"
		elif node == self.outputLayer[3]:
			return "chi_m"

	def getExpected(self,node,phoneme):
		if phoneme[1] == "a_f":
			if node == self.outputLayer[0]:
				expected = 1
			else:
				expected = 0
		elif phoneme[1] == "a_m":
			if node == self.outputLayer[1]:
				expected = 1
			else:
				expected = 0
		elif phoneme[1] == "chi_f":
			if node == self.outputLayer[2]:
				expected = 1
			else:
				expected = 0
		elif phoneme[1] == "chi_m":
			if node == self.outputLayer[3]:
				expected = 1
			else:
				expected = 0
		return expected

	def trainingEpoch(self):
		file_ = 0
		for phoneme in self.inputActivations:
			output = self.minusPhase(phoneme)	
			if self.plusPhase(phoneme,output) == False:
				self.epochError += 1
				#self.stateList.append(False)
			#else:
				#self.stateList.append(True)

	def minusPhase(self,phoneme):
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
		return max(layerActivity, key = lambda x: x[1])
	
	def checkMinusPhaseOutput(self,phoneme,minusPhaseOutput):
		expected = self.getExpected(minusPhaseOutput[0],phoneme)
		phon = self.getPhoneme(minusPhaseOutput[0])
		#if minusPhaseOutput[0] == self.outputLayer[0]:
		#	phon = "a_f"
		#elif minusPhaseOutput[0] == self.outputLayer[1]:
		#	phon = "a_m"
		#print "Expected:", phoneme[1], "Output:", phon, "Node:", choice[0], "Activation:", choice[1]			
		#print "a_f unit activation: ",self.outputLayer[0].act
		#print "a_m unit activation: ",self.outputLayer[1].act
		correct = False
		if phoneme[1] == phon:
			correct = True
		return correct, phon		

	def plusPhase(self,phoneme,minusPhaseOutput):
		#for node, act in layerActivity:
			#print "node: ", node, "act: ", act
		#layerActivity.remove(choice)
		correct, phon = self.checkMinusPhaseOutput(phoneme,minusPhaseOutput)

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
			return False
		else:
			return True

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

	def loadWeights(self):
		file_ = raw_input("Enter name of weights file: ")
		file_ = open(file_,"r")
		weights = []
		for weight in file_:
			weights.append(float(weight)) 
		file_.close()
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				input_node.hiddenConnections.append((hidden_node,weights[0]))
				hidden_node.inputConnections.append((input_node,weights[0]))
				weights.pop(0)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				hidden_node.outputConnections.append((output_node,weights[0]))
				output_node.hiddenConnections.append((hidden_node,weights[0]))
				weights.pop(0)

	def train(self):
		self.epochError = 0
		for i in range(100):
			self.trainingEpoch()
			self.epochs += 1
		print self.epochError
		if self.epochError < 1:
			return
		else:
			return self.train()

	def test(self):
		trial = 0
		#tts = gTTS(text="Expected output", lang="en")
		#tts.save("expected_output.mp3")
		#tts = gTTS(text="Output", lang="en")	
		#tts.save("output.mp3")
		#tts = gTTS(text="Trial", lang="en")
		#tts.save("trial.mp3")
		for activation, phoneme in self.inputActivations:
			#tts = gTTS(text=trial, lang = "en")
			#tts.save(trial+".mp3")
			#subprocess.call(["mpg321", "trial.mp3", "-quiet"], stderr=None, shell=False)
			os.system("mpg321 trial.mp3 --quiet") 
			os.system("mpg321 " + str(trial) + ".mp3 " + "--quiet")
			os.system("mpg321 expected_output.mp3 --quiet")
			os.system("mpg321 japanese_mp3s/" + phoneme + ".mp3 " + "--quiet")
			print "\nTrial: ", trial
			print "Phoneme: ", phoneme[:-2]
			print "Gender: ", phoneme[-1:]
			output = self.minusPhase((activation,phoneme))
			correct, phon = self.checkMinusPhaseOutput((activation,phoneme),output)
			if correct == True:
				print "Correct!", "Output: ", phon
			else:
				print "Test failed.", "Output: ", phon
			os.system("mpg321 output.mp3 --quiet")
			os.system("mpg321 japanese_mp3s/" + phon + ".mp3 " + "--quiet")
			trial += 1

	def saveWeights(self):
		weights = open(raw_input("Enter file name: "),"w")
		for node in self.inputLayer:
			for hidden_node, connection in node.hiddenConnections:
				weights.write(str(connection))
				weights.write("\n")
		for node in self.hiddenLayer:
			for output_node, connection in node.outputConnections:
				weights.write(str(connection))
				weights.write("\n")
		weights.close()

def main():
	net = NeuralNetwork()
	net.makeNetwork()
	net.genInputActivations()
	if raw_input("Would you like to load weights? (y/n) ") == "y":
		net.loadWeights()
	else:
		net.initializeRandomWeights()
		try:
			net.train()
			print "Error across 100 epochs: ", net.epochError
			print "Epochs to convergence:", net.epochs
			#print net.stateList
		except RuntimeError:
			print "Training Failed"
	net.test()
	if raw_input("Would you like to save the network's weights? (y/n) ") == "y":
		net.saveWeights()	

if __name__=="__main__":
	main()
