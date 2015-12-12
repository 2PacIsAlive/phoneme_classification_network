#!usr/bin/env python

import glob
from pyprocessing import *

class ReceptiveFields():
	def __init__(self):
		self.files = []
		self.index = 0

	def loadFiles(self):
		self.files = [x for x in glob.glob("*.data")]

	def incrementFileIndex(self):
		self.index += 1	
		print "class", self.index

def setup():
	size(500,500)
	#noStroke()

def draw():
	background(0)
	data = open(rfs.files[rfs.index],"r").readlines()
	data = [x[:-2] for x in data]
	x = 0
	y = 0
	#print "drawing weights..."
	for weight in data:
		if float(weight) < 0:
			B_color = int(abs(float(weight)*100))
			R_color = 50
		else:
			B_color = 50
			R_color = int(float(weight)*100)
		stroke(R_color,50,B_color)
		fill(B_color,50,R_color)
		rectMode(CORNER)
		rect(x,y,100,100)
		if x == 700:
			x = 0
			y += 100
		else:
			x += 100

	#print "finished"
	#data.close()
	save(str(rfs.index)+".png")
	#print "saved"
	#data.pop(0)
	rfs.index += 1
	#print rfs.index

if __name__=="__main__":
	rfs = ReceptiveFields()
	rfs.loadFiles()
	run()
