#!usr/bin/env python

from pylab import *
from scipy.io import wavfile


def genFFT(phoneme):
	frequency, sound = wavfile.read(phoneme)
	sound = sound/(2.**15)
	print sound.dtype
	s1 = sound[:,0]
	time = arange(0, 5060.0, 1)
	time = time/frequency
	time *= 1000
	plot(time, s1, color='k')
	ylabel('Amplitude')
	xlabel('Time (ms)')

def main():
	phonemes = ["test.wav"]
	for phoneme in phonemes:
		genFFT(phoneme)

if __name__=="__main__":
	main()
