import numpy
def smooth(x, window_len=11, window='hanning'):
	"""smooth the data using a window with requested size.

	This method is based on the convolution of a scaled window with the signal.
	The signal is prepared by introducing reflected copies of the signal 
	(with the window size) in both ends so that transient parts are minimized
	in the begining and end part of the output signal.
	
	input:
		x: the input signal 
		window_len: the dimension of the smoothing window; should be an odd integer
		window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
			flat window will produce a moving average smoothing.
	
	output:
		the smoothed signal
	
	example:
	
	t=linspace(-2,2,0.1)
	x=sin(t)+randn(len(t))*0.1
	y=smooth(x)
	
	see also: 
	
	numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
	scipy.signal.lfilter
	
	TODO: the window parameter could be the window itself if an array instead of a string   
	"""
	
	if x.ndim != 1:
		raise ValueError, "smooth only accepts 1 dimension arrays."
	
	if x.size < window_len:
		raise ValueError, "Input vector needs to be bigger than window size."
	
	if window_len < 3:
		return x
	
	if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
		raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
	
	s = numpy.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
	
	if window == 'flat': #moving average
		w = numpy.ones(window_len,'d')
	else:
		w = eval('numpy.'+window+'(window_len)')
	
	y = numpy.convolve(w/w.sum(), s, mode='same')
	return y[window_len:-window_len+1]


def hls_sort2(a, b):
	a = a[0]
	b = b[0]
	
	if a[1] > b[1]: # L
		return 1
	elif a[1] < b[1]:
		return -1
	else:
		if a[0] > b[0]: # H
			return 1
		elif a[0] < b[0]:
			return -1
		else:
			if a[2] > b[2]: # S
				return 1
			elif a[2] < b[2]:
				return -1
			else:
				return 0
	



"""def hls_sort(a, b): # HLS
	if a[1] > b[1]: # L
		return 1
	elif a[1] < b[1]:
		return -1
	else:
		if a[0] > b[0]: # H
			return 1
		elif a[0] < b[0]:
			return -1
		else:
			if a[2] > b[2]: # S
				return 1
			elif a[2] < b[2]:
				return -1
			else:
				return 0


def hsv_sort(a, b): # HSV
	if a[2] > b[2]: # V
		return 1
	elif a[2] < b[2]:
		return -1
	else:
		if a[0] > b[0]: # H
			return 1
		elif a[0] < b[0]:
			return -1
		else:
			if a[1] > b[1]: # S
				return 1
			elif a[1] < b[1]:
				return -1
			else:
				return 0"""

import math
def timecode_to_seconds(tc):
	# 00:12:34,567
	h = int(tc[0:2])
	m = int(tc[3:5])
	s = int(tc[6:8])
	milli = int(tc[-3:])
	return (milli/1000.0) + s + (m*60) + (h*60*60)


def seconds_to_timecode(s):
	h = int(math.floor(float(s) / (60*60)))
	m = int(math.floor(float(s) % (60*60)) / 60)	
	s = s - (m*60) - (h*60*60)
	
	if h > 10:
		h = str(h)
	else:
		h = "0" + str(h)
	
	if m > 10:
		m = str(m)
	else:
		m = "0" + str(m)
	
	if s > 10:
		s = str(s)
	else:
		s = "0" + str(s)
		
	s = s.replace('.', ',')[:6]
	s = s + (6 - len(s)) * "0"
	
	return h + ":" + m + ":" + s