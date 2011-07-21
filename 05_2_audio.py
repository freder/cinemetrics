# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import wave
import scipy.io.wavfile
import numpy
import numpy.fft
import math
import xml.etree.ElementTree as et
import os
import os.path

from lib import smooth


# http://onlamp.com/pub/a/python/2001/01/31/numerically.html?page=1
# http://xoomer.virgilio.it/sam_psy/psych/sound_proc/sound_proc_python.html
# dB:  http://www.dsprelated.com/showmessage/29246/1.php
# RMS: http://www.opamp-electronics.com/tutorials/measurements_of_ac_magnitude_2_01_03.htm
# http://www.audioforums.com/forums/showthread.php?11942-extract-volume-out-of-wave-file&p=54594#post54594


def main():
	os.chdir(sys.argv[1])
	f_out = open("smooth_audio.txt", "w")
	
	tree = et.parse("project.xml")
	movie = tree.getroot()
	path = movie.attrib["path"]
	path = os.path.dirname(path)
	fps = float( movie.attrib["fps"] )
	
	os.chdir(path)
	file = os.path.join(path, "audio_trimmed.wav")
	print file

	f = wave.open(file, "rb")
	bit = f.getsampwidth() * 8
	print bit, "bit" # usually: signed 16 bit [-32768, 32767]
	f.close()

	rate, data = scipy.io.wavfile.read(file)
	print rate, "hz"
	# http://en.wikipedia.org/wiki/Sound_level_meter#Exponentially_averaging_sound_level_meter
	chunk = rate / 8 #25

	#print max(data)
	#print min(data)

	max = numpy.max( numpy.absolute(data) )

	"""fft = numpy.fft.rfft(data, chunk)
	fft = numpy.absolute(fft)
	print fft
	plt.plot(fft)
	plt.show()"""

	data_db = numpy.array([])
	data_rms = numpy.array([])
	for i in range(len(data) / chunk):
		values = numpy.array( data[i*chunk : (i+1)*chunk] )
		
		# normalize [0, 1]
		#values = values / 2**(bit-1)
		values = values / float(max)
		
		#values = values * float(1) # why do I need that?
		
		# root mean square
		values = numpy.power(values, 2)
		rms = numpy.sqrt( numpy.mean(values) )
		data_rms = numpy.append(data_rms, rms)
		
		# decibel
		db = 20 * numpy.log10( (1e-20+rms) ) #/ float(max)
		data_db = numpy.append(data_db, db)

	#plt.ylim(-60, 0)
	
	#plt.plot( smooth(data_rms/numpy.max(data_rms), window_len=rate/(fps*2)), "k-" )
	#plt.plot(smooth(data_db, window_len=rate/fps), "g-")
	
	smooth_db = 1 + smooth(data_db, window_len=rate/(fps*3)) / (60.0) # [0..1]
	plt.ylim(0, 1)
	plt.plot(smooth_db, "g-")
	
	for item in smooth_db:
		if item < 0:
			item = 0
		f_out.write("%f\n" % float(item))
	f_out.close()
	
	
	#plt.plot(data_db)
	
	plt.show()



#for i in range(len(data) / (rate*250)):
#	plt.specgram(data[i*rate*250 : (i+1)*rate*250], Fs = rate, scale_by_freq=True, sides='default')
#	plt.show()
	





"""def show_wave_n_spec(speech):
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

show_wave_n_spec(fil)"""




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




"""
values = []
for i in range(len(data) / chunk):
	x = 
	db = 20 * numpy.log10(1e-20 + numpy.absolute(x))
	mean = numpy.mean(db)
	values.append(mean)

values = numpy.array(values)
smooth_values = smooth(values, window_len=rate/5)
smooth_values2 = smooth(values, window_len=rate/10)

plt.ylim(-100, 100)
plt.plot(smooth_values)
plt.plot(smooth_values2, "r-")
plt.show()
"""





"""import numpy.fft
spectrum = numpy.fft.fft(data[:10000])
frequencies = numpy.fft.fftfreq(len(data[:10000]))
plt.plot(frequencies,spectrum)
plt.show()"""


# #########################
if __name__ == "__main__":
	main()
# #########################
