
from pylab import gca, plot, show, title, xlabel, ylabel, subplot, subplots, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
from scipy.io.wavfile import read,write
import glob

def plotSpectru(y,Fs):
 n = len(y) # lungime semnal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = frq[range(n/2)] # one side frequency range

 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(n/2)]
 
 plot(frq,abs(Y),'r') # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')

Fs = 44100;  # sampling rate

for file_ in glob.glob("japanese/*"):
	
	rate,data=read(file_)
	y=data[:,1]
	lungime=len(y)
	timp=len(y)/44100.
	t=linspace(0,timp,len(y))

	#subplot(2,1,1)
	#plot(t,y)
	#title(file_)
	#xlabel('Time')
	#ylabel('Amplitude')
	#subplot(2,1,2)
	plotSpectru(y,Fs)
	
	ax = gca()
	ax.yaxis.set_visible(False)
	ax.xaxis.set_visible(False)
	ax.axis('off')

	#show()
	file_ = file_[9:-4]
	if file_[-1] == "f":
		savefig("japanese_ffts_female/"+file_)
	else:
		savefig("japanese_ffts_male/"+file_)
