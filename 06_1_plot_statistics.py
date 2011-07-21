# -*- coding: utf-8 -*-
import sys
import os
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import math
import numpy

from lib import smooth


OUTPUT_DIR_NAME = "plots"


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except OSError:
		pass
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	fps = float( movie.attrib["fps"] )
	frames = float( movie.attrib["frames"] )
	
	os.chdir(OUTPUT_DIR_NAME)
	
	s = frames / fps
	m = s / 60.0
	print s, "seconds"
	h = s / float(60*60)
	print "%.2f hours" % h
	percent = h / 2.0
	print "%.2f %%" % percent
	print "%d:%02d" % (math.floor(h), (h-math.floor(h))*60)
	
	# ===== DURATION ==================================================================================================
	plt.axis(ymin=0, ymax=10, xmin=0, xmax=3*60)
	plt.xlabel("%d mins, %.2f %% of 2 hours" % (s / 60, percent))
	
	lw = 20
	plt.plot([0, 2*60], [1, 1], "k-", linewidth=lw, solid_capstyle="butt")
	plt.plot([0, h*60], [2, 2], "b-", linewidth=lw, solid_capstyle="butt")
	
	r = 200 / 2
	r2 = math.sqrt( percent * r*r )
	plt.plot([100], [6], "o", markeredgewidth=0, markersize=2*r2, markerfacecolor="b")
	plt.plot([100], [6], "o", markeredgewidth=1, markersize=2*r, markerfacecolor="none")
	
	plt.axis("off")
	plt.show()
	#plt.savefig(os.path.join(OUTPUT_DIR_NAME, "duration.ps"))
	
	# ===== TRENDLINES ==================================================================================================
	f = open("..\\motion_shot-avg.txt", "r")
	values = [[float(values[0]), int(values[1])] for values in [line.split("\t") for line in f if line]]
	f.close()
	
	motions, durations = ([a for a, b in values], [b for a, b in values])
	durations_sec = [float(d/fps) for d in durations]
	
	print len(durations), "shots"
	print "%.1f cuts per minute" % (len(durations)/m)
	print "min:", min(durations_sec), "s"
	print "max:", max(durations_sec), "s"
	print "range:", max(durations_sec)-min(durations_sec), "s"
	print "asl:", numpy.mean(durations_sec), "s"
	print "std:", numpy.std(durations_sec), "s"
	print "var:", numpy.var(durations_sec), "s"
	
	file = open("..\\subtitles.txt")
	s = file.read()
	file.close()
	word_count = len( s.split() )
	words_per_minute = word_count / m
	print words_per_minute, "words / minute"
	
	WINDOW_LEN = 20
	TREND_DEGREE = 1 # polynom 1ten grades
	
	data = numpy.array(WINDOW_LEN*[durations_sec[0]] + durations_sec + WINDOW_LEN*[0])
	trend_duration = numpy.polyfit(range(len(data)), data, TREND_DEGREE)
	trend_duration = numpy.poly1d(trend_duration)
	smooth_data = smooth( data, window_len=WINDOW_LEN, window='hanning' )
	plt.axis(ymin=0, ymax=60.0, xmin=0, xmax=len(durations_sec)-1)
	plt.plot(smooth_data[WINDOW_LEN:-WINDOW_LEN], "r-", label="shot length (in seconds)")
	plt.plot(trend_duration(numpy.arange(len(data))), "m-", label="shot length trend")
	plt.legend(loc="upper left")
	
	data = numpy.array(WINDOW_LEN*[motions[0]] + motions + WINDOW_LEN*[0])
	trend_motion = numpy.polyfit(range(len(data)), data, TREND_DEGREE)
	trend_motion = numpy.poly1d(trend_motion)
	smooth_data = smooth(data, window_len=WINDOW_LEN, window='hanning')
	plt.xlabel("shot / %d" % (len(durations)))
	plt.twinx()
	plt.axis(ymin=0, ymax=1.0)
	plt.plot(smooth_data[WINDOW_LEN:-WINDOW_LEN], "b-", label="motion (0..1)")
	plt.plot(trend_motion(numpy.arange(len(data))), "c-", label="motion trend")
	plt.legend(loc="upper right")
	
	plt.show()
	
	# ===== TEST ==================================================================================================
	if False:
		smooth_duration = 0.5 * smooth_data / numpy.max(smooth_data)
		smooth_deriv = 100 * smooth( numpy.diff( smooth_data ), window_len=10*WINDOW_LEN )[WINDOW_LEN:-WINDOW_LEN]
		smooth_motion = smooth_data[WINDOW_LEN:-WINDOW_LEN]
		
		'''for x, y in enumerate(smooth_deriv):
			m = smooth_motion[x]
			if x % 2 == 0:
				plt.vlines(x, y-m, y+m, lw=m*2)
		
		plt.plot(smooth_deriv, "w-", lw=1)
		mini = min(len(smooth_deriv), len(smooth_motion))
		plt.fill_between(range(mini), smooth_deriv[:mini], smooth_deriv[:mini]+smooth_motion[mini], color="y")
		plt.axis(ymin=-1, ymax=1, xmin=0, xmax=len(durations_sec)-1)
		plt.show()'''
		
		
		# audio
		f = open("..\\smooth_audio.txt", "r")
		values = [float(line) for line in f if line]
		f.close()
		audio_step = float(len(values)) / float(len(smooth_deriv))
		audio_counter = 0
		
		
		fig = plt.figure()
		ax = fig.add_subplot(111, polar=True)
		
		STEP = math.ceil(0.01* len(smooth_deriv) / float(2*math.pi) )
		
		for x, y in enumerate(smooth_deriv):
			if x % STEP == 0:
				x = 2*math.pi * float(x) / len(smooth_deriv)
				y += 2
				audio_value = 0.75 * values[int( audio_counter * audio_step )]
				ax.vlines(x, y+0.01, y+0.01+audio_value, lw=audio_value*2, color="y")
				audio_counter += 1
		
		for x, y in enumerate(smooth_deriv):
			m = smooth_motion[x]
			#d = smooth_duration[x]
			if x % STEP == 0:
				x = 2*math.pi * float(x) / len(smooth_deriv)
				y += 2
				ax.vlines(x, y+0.01, y+0.01+m, lw=m*2)
				
				"""audio_value = 0.75 * values[int( audio_counter * audio_step )]
				ax.vlines(x, y-0.01, y-0.01-audio_value, lw=audio_value*2)
				audio_counter += 1"""
		
		plt.show()
	
	# ===== RADAR ==================================================================================================
	asl = numpy.mean(durations)
	std = numpy.std(durations)
	avg_motion = numpy.mean(motions)
	
	properties = {}
	properties["duration"] = percent
	#properties["average shot length"] = 0.1 * asl / float(fps)
	properties["cuts / minute"] = (len(durations) / m) / 20.0
	properties["average motion"] = avg_motion / 0.25
	properties["words / minute"] = words_per_minute / 60.0
	properties["average loudness"] = 0.5

	angle_step = 360.0 / len(properties)
	angles = []
	for i in range(len(properties)):
		angles.append(math.radians(i*angle_step))
		
	fig = plt.figure()
	ax = fig.add_subplot(111, polar=True)
	ax.set_rmax(5.0)
	ax.set_xticks([i*2*math.pi/len(properties) for i in range(len(properties))])
	ax.set_xticklabels(properties.keys())
	ax.plot(angles, properties.values())
	for i in range(len(properties)):
		ax.vlines(angles[i], 0, properties[properties.keys()[i]], lw=15)
	#ax.axis("off")
	plt.show()
	
	# ===== SHOTS ==================================================================================================
	f = open("..\\shots.txt", "r")
	values = [[int(values[0]), int(values[1]), int(values[2])] for values in [line.split("\t") for line in f if line]]
	f.close()
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.ylim(ymin=5, ymax=15.5)
	#ax.set_yscale("log")
	for i, item in enumerate(values):
		#print item
		frame_start, frame_end, length = item
		y = 10
		if i % 2 == 0:
			color = (0, 0, 0)
		else:
			color = (0.5, 0.5, 0.5)
			y = 10.5
		#ax.hlines(length/100.0, frame_start, frame_end, color=color, lw=100)
		ax.hlines(y, frame_start, frame_end, color=color, lw=30)
	
	ax.axis("off")
	plt.show()
	
	"""
	# ===== COLOR ==================================================================================================
	f = open("colors.txt", "r")
	colors = [[int(values[0]), int(values[1]), int(values[2]), int(values[3])] for values in [line.split(", ") for line in f if line]]
	f.close()
	
	#print colors
	x = numpy.arange(0, 2*math.pi, 2*math.pi/len(colors))
	#print x
	
	y = [values[3] for values in [color for color in colors]]
	#print y
	total = sum(y)
	for i, yps in enumerate(y):
		faktor = float(yps) / total
		y[i] = math.sqrt(faktor * total*total)
	
	fig = plt.figure()
	ax = fig.add_subplot(111, polar=True)
	for i, color in enumerate(colors):
		ax.bar(x[i], y[i], width=0.2*math.pi, edgecolor="none", color=(color[0]/255.0, color[1]/255.0, color[2]/255.0))
	ax.axis("off")
	plt.show()
	"""
	
	#raw_input("- done -")
	return



# #########################
if __name__ == "__main__":
	main()
# #########################
