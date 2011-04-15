#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
import wave
import numpy
import struct
import math

def show_wave_n_spec(speech):
	spf = wave.open(speech, "r")
	#sound_info = spf.readframes(-1)
	sound_info = spf.readframes(1000000)
	sound_info = numpy.fromstring(sound_info, 'Int16')
	
	f = spf.getframerate()
	
	plt.subplot(211)
	plt.plot(sound_info)
	plt.title('Wave from and spectrogram of %s' % sys.argv[1])
	
	plt.subplot(212)
	spectrogram = plt.specgram(sound_info, Fs = f, scale_by_freq=True, sides='default')
	
	plt.show()
	spf.close()


#show_wave_n_spec(fil)


file = sys.argv[1]
"""
f = wave.open(file, "rb")
wav_params = f.getparams()
print wav_params
#sample_rate = wav_params[2]
sample_rate = f.getframerate()

volumes = []
chunk_size = 10 #sample_rate / 25

while True:
	data_string = f.readframes(chunk_size)
	unpacked = struct.unpack("%dB" % len(data_string), data_string)
	
	if not unpacked:
		break
	
	chunk = numpy.array(unpacked)
	#print chunk
	chunk = pow(abs(chunk), 2)
	rms = math.sqrt(chunk.mean())
	#print rms
	#db = 10 * math.log10(1e-20 + rms)
	#print db
	
	volumes.append(rms)

#plt.plot(volumes)
plt.specgram(volumes)
plt.show()
f.close()"""

import scipy
import scipy.io.wavfile
rate, data = scipy.io.wavfile.read(file)
#data = data[:len(data)/10]
print rate
chunk = rate / 25

values = []
for i in range(1 + len(data) / chunk):
	x = scipy.fft(data[i*chunk:(i+1)*chunk])
	db = 20 * scipy.log10(1e-20 + scipy.absolute(x))
	# average volume per chunk
	mean = numpy.mean(db)
	values.append(mean)

from lib import smooth

values = numpy.array(values)
smooth_values = smooth(values, window_len=rate/5)
smooth_values2 = smooth(values, window_len=rate/10)

#for v in smooth_values:
#	print v

plt.ylim(0, 100)
plt.plot(smooth_values)
plt.plot(smooth_values2, "r-")
plt.show()

#for item in data:
	#print item

"""import numpy.fft
spectrum = numpy.fft.fft(data[:10000])
frequencies = numpy.fft.fftfreq(len(data[:10000]))
plt.plot(frequencies,spectrum)
plt.show()"""


