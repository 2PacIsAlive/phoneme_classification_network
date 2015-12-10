#!usr/bin/env python

from PIL import Image
#from gtts import gTTS
import random
import glob
import math
import os

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
		for hidden_node in range(14):
			self.hiddenLayer.append(Neuron())
		for output_node in range(12):
			self.outputLayer.append(Neuron())	

	def genInputActivations(self):
		for file_ in glob.glob("gentask/*"):	
			phoneme = Image.open(file_)
			pix = list(phoneme.getdata())
			activation = []
			for pixel in pix:
				hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
				activation.append((int(hexval,16))/100000.0)
			self.inputActivations.append((activation,file_[8:-4]))

	def sigmoid(self,activation):
		try:
			return 1 / (1 + math.exp(-activation))	
		except OverflowError:
			return 0 
	
	def hiddenActivationFunction(self,node,index):
		xw = 0
		#zw = 0
		for input_node in self.inputLayer:
			xw += input_node.hiddenConnections[index] * float(input_node.act) 
		#for output_node in self.outputLayer:
		#	zw += output_node.hiddenConnections[index] * float(input_node.act)
		#return self.sigmoid(xw + zw)
		return self.sigmoid(xw)

	def outputActivationFunction(self,node,index):
		f = 0
		for hidden_node in self.hiddenLayer:
			f += hidden_node.outputConnections[index] * float(hidden_node.act)
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
		elif node == self.outputLayer[4]:
			return "e_f"
		elif node == self.outputLayer[5]:
			return "e_m"
		elif node == self.outputLayer[6]:
			return "fu_f"
		elif node == self.outputLayer[7]:
			return "fu_m"
		elif node == self.outputLayer[8]:
			return "ha_f"
		elif node == self.outputLayer[9]:
			return "ha_m"
		elif node == self.outputLayer[10]:
			return "he_f"
		elif node == self.outputLayer[11]:
			return "he_m"
		'''
		elif node == self.outputLayer[12]:
			return "hi_f"
		elif node == self.outputLayer[13]:
			return "hi_m"
		elif node == self.outputLayer[14]:
			return "ho_f"
		elif node == self.outputLayer[15]:
			return "ho_m"
		elif node == self.outputLayer[16]:
			return "i_f"
		elif node == self.outputLayer[17]:
			return "i_m"
		elif node == self.outputLayer[18]:
			return "ka_f"
		elif node == self.outputLayer[19]:
			return "ka_m"
		elif node == self.outputLayer[20]:
			return "ke_f"
		elif node == self.outputLayer[21]:
			return "ke_m"
		elif node == self.outputLayer[22]:
			return "ki_f"
		elif node == self.outputLayer[23]:
			return "ki_m"
		elif node == self.outputLayer[24]:
			return "ko_f"
		elif node == self.outputLayer[25]:
			return "ko_m"
		elif node == self.outputLayer[26]:
			return "ku_f"
		elif node == self.outputLayer[27]:
			return "ku_m"
		elif node == self.outputLayer[28]:
			return "ma_f"
		elif node == self.outputLayer[29]:
			return "ma_m"
		elif node == self.outputLayer[30]:
			return "me_f"
		elif node == self.outputLayer[31]:
			return "me_m"
		elif node == self.outputLayer[32]:
			return "mi_f"
		elif node == self.outputLayer[33]:
			return "mi_m"
		'''
	def getExpected(self,node,phoneme):
		if phoneme[1] == "a_f":
			if node == self.outputLayer[0]:
				return 1
			else:
				return 0
		elif phoneme[1] == "a_m":
			if node == self.outputLayer[1]:
				return 1
			else:
				return 0
		elif phoneme[1] == "chi_f":
			if node == self.outputLayer[2]:
				return 1
			else:
				return 0
		elif phoneme[1] == "chi_m":
			if node == self.outputLayer[3]:
				return 1
			else:
				return 0
		elif phoneme[1] == "e_f":
			if node == self.outputLayer[4]:
				return 1
			else:
				return 0
		elif phoneme[1] == "e_m":
			if node == self.outputLayer[5]:
				return 1
			else:
				return 0
		elif phoneme[1] == "fu_f":
			if node == self.outputLayer[6]:
				return 1
			else:
				return 0
		elif phoneme[1] == "fu_m":
			if node == self.outputLayer[7]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ha_f":
			if node == self.outputLayer[8]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ha_m":
			if node == self.outputLayer[9]:
				return 1
			else:
				return 0
		elif phoneme[1] == "he_f":
			if node == self.outputLayer[10]:
				return 1
			else:
				return 0
		elif phoneme[1] == "he_m":
			if node == self.outputLayer[11]:
				return 1
			else:
				return 0
		'''
		elif phoneme[1] == "hi_f":
			if node == self.outputLayer[12]:
				return 1
			else:
				return 0
		elif phoneme[1] == "hi_m":
			if node == self.outputLayer[13]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ho_f":
			if node == self.outputLayer[14]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ho_m":
			if node == self.outputLayer[15]:
				return 1
			else:
				return 0
		elif phoneme[1] == "i_f":
			if node == self.outputLayer[16]:
				return 1
			else:
				return 0
		elif phoneme[1] == "i_m":
			if node == self.outputLayer[17]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ka_f":
			if node == self.outputLayer[18]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ka_m":
			if node == self.outputLayer[19]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ke_f":
			if node == self.outputLayer[20]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ke_m":
			if node == self.outputLayer[21]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ki_f":
			if node == self.outputLayer[22]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ki_m":
			if node == self.outputLayer[23]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ko_f":
			if node == self.outputLayer[24]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ko_m":
			if node == self.outputLayer[25]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ku_f":
			if node == self.outputLayer[26]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ku_m":
			if node == self.outputLayer[27]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ma_f":
			if node == self.outputLayer[28]:
				return 1
			else:
				return 0
		elif phoneme[1] == "ma_m":
			if node == self.outputLayer[29]:
				return 1
			else:
				return 0
		elif phoneme[1] == "me_f":
			if node == self.outputLayer[30]:
				return 1
			else:
				return 0
		elif phoneme[1] == "me_m":
			if node == self.outputLayer[31]:
				return 1
			else:
				return 0
		elif phoneme[1] == "mi_f":
			if node == self.outputLayer[32]:
				return 1
			else:
				return 0
		elif phoneme[1] == "mi_m":
			if node == self.outputLayer[33]:
				return 1
			else:
				return 0
		'''
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
				#the change in weights for each output/hidden connection are:
					#the error for the output node (expected - output) multiplied by the activation of the unit
				new_weight = (hidden.act * error) + output.hiddenConnections[hiddenCounter]
				#new_weight = (hidden.act * 0.05 * error) + output.hiddenConnections[hiddenCounter][1]
				#print output, correct, "old: ", output.hiddenConnections[hiddenCounter][1], "new: ",new_weight
				output.hiddenConnections[hiddenCounter] = new_weight
				hidden.outputConnections[outputCounter] = new_weight
				#error = self.getExpected(output,phoneme) - hidden.act
				#print error, hidden.act, output.act
				inputCounter = 0
				for input_ in self.inputLayer:
					#the change in weights for each input node are:
						#the sum over all hidden units of:
							#the expected output multiplied by the weight for the hidden/input pair
						#minus the sum over all hidden units of:
							#the output unit's activation multiplied by the weight for the hidden/input pair
						#multiplied by yprime????
							#I think y prime is the activation of the hidden layer unit
					backprop_counter = 0
					tw = 0
					zw = 0
					for output_backprop in self.outputLayer:
						weight = output_backprop.hiddenConnections[hiddenCounter]
						tw += self.getExpected(output_backprop,phoneme) * weight 
						zw += output_backprop.act * weight
						backprop_counter += 1
					#new_weight = ((tw - zw) * hidden.act * input_.act) + hidden.inputConnections[inputCounter]
					new_weight = ((tw - zw) * (hidden.act * (1 - hidden.act) * input_.act)) + hidden.inputConnections[inputCounter]
					#print "EXPECTED:", self.getExpected(output,phoneme), "ACTUAL:", output.act, "OLD:", hidden.inputConnections[inputCounter], "NEW:", new_weight
					#new_weight = (input_.act * 0.05 * error) + hidden.inputConnections[inputCounter][1]
					hidden.inputConnections[inputCounter] = new_weight
					input_.hiddenConnections[hiddenCounter] = new_weight
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
				#input_node.hiddenConnections.append((hidden_node,randomWeight))
				input_node.hiddenConnections.append(randomWeight)
				#hidden_node.inputConnections.append((input_node,randomWeight))
				hidden_node.inputConnections.append(randomWeight)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				randomWeight = random.uniform(-1,1)
				#hidden_node.outputConnections.append((output_node,randomWeight))
				hidden_node.outputConnections.append(randomWeight)
				#output_node.hiddenConnections.append((hidden_node,randomWeight))
				output_node.hiddenConnections.append(randomWeight)

	def loadWeights(self):
		file_ = raw_input("Enter name of weights file: ")
		file_ = open(file_,"r")
		weights = []
		for weight in file_:
			weights.append(float(weight)) 
		file_.close()
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				#input_node.hiddenConnections.append((hidden_node,weights[0]))
				input_node.hiddenConnections.append(weights[0])
				#hidden_node.inputConnections.append((input_node,weights[0]))
				hidden_node.inputConnections.append(weights[0])
				weights.pop(0)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				#hidden_node.outputConnections.append((output_node,weights[0]))
				hidden_node.outputConnections.append(weights[0])
				#output_node.hiddenConnections.append((hidden_node,weights[0]))
				output_node.hiddenConnections.append(weights[0])
				weights.pop(0)

	def train(self):
		self.epochError = 0
		#for i in range(10):
		#	self.trainingEpoch()
		#	self.epochs += 1
		self.trainingEpoch()
		self.epochs += 1
		print "Epoch:", self.epochs, "Error:", 100 * float(self.epochError)/float(len(self.outputLayer))
		#print self.epochError
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
			if verbose:
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
			if verbose:
				os.system("mpg321 output.mp3 --quiet")
				os.system("mpg321 japanese_mp3s/" + phon + ".mp3 " + "--quiet")
			trial += 1

	def saveWeights(self):
		weights = open(raw_input("Enter file name: "),"w")
		#weights = open("weights_16.data","w")
		for node in self.inputLayer:
			for connection in node.hiddenConnections:
				weights.write(str(connection))
				weights.write("\n")
		for node in self.hiddenLayer:
			for connection in node.outputConnections:
				weights.write(str(connection))
				weights.write("\n")
		weights.close()

def main():
	#net = NeuralNetwork()
	net.makeNetwork()
	print "generating input activations...\n"
	net.genInputActivations()
	if raw_input("Would you like to load weights? (y/n) ") == "y":
		print "loading weights...\n"
		net.loadWeights()
	else:
		print "initializing random weights...\n"
		net.initializeRandomWeights()
		try:
			net.test()
			print "beginning training...\n"
			net.train()
			print "Success!"
			print "Error across 100 epochs: ", net.epochError
			print "Epochs to convergence:", net.epochs
			#print net.stateList
		except:
			print "training failed"
	print "testing network...\n"
	net.test()
	#if raw_input("Would you like to save the network's weights? (y/n) ") == "y":
	#	net.saveWeights()	
	if raw_input("Would you like to save weights? (y/n) ") == "y":
		net.saveWeights()
		print "weights saved\n"

if __name__=="__main__":
	net = NeuralNetwork()
	verbose = False
	main()
