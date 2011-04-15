# -*- coding: utf-8 -*-
import cv
import numpy
import scipy.cluster
import os
import sys
import xml.etree.ElementTree as et
import time
import math

from lib import hls_sort2


def unique(seq, idfun=None): 
	if idfun is None:
		def idfun(x): return x
	seen = {}
	result = []
	for item in seq:
		marker = idfun(item)
		if marker in seen: continue
		seen[marker] = 1
		result.append(item)
	return result


def unique2(seq):
	checked = []
	for e in seq:
		if e not in checked:
			checked.append(e)
	return checked


DEBUG = False

NUM_CLUSTERS = 5
PIXELS_PER_COLOR = 20
EVERY_NTH_FRAME = 5
OUTPUT_DIR_NAME = "shot_colors"


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except:
		pass
	
	tree = et.parse("project.xml")
	movie = tree.getroot()
	file_path = movie.attrib["path"]
	cap = cv.CreateFileCapture(file_path)
	cv.QueryFrame(cap)
	
	if DEBUG:
		cv.NamedWindow("win", cv.CV_WINDOW_AUTOSIZE)
		cv.MoveWindow("win", 200, 200)

	t = time.time()
	
	f = open("shots.txt", "r")
	scene_durations = [int(values[2]) for values in [line.split("\t") for line in f if line]]
	f.close()
	
	for scene_nr, duration in enumerate(scene_durations):
		print "shot #%d" % scene_nr, "/", len(scene_durations)-1
		
		h = int( math.ceil( float(duration) / EVERY_NTH_FRAME ) )
		output_img = cv.CreateImage((PIXELS_PER_COLOR*NUM_CLUSTERS, h), cv.IPL_DEPTH_8U, 3)
		frame_counter = 0
		
		for i in range(duration):
			img_orig = cv.QueryFrame(cap)
			if not img_orig: # eof
				break
			
			if i % EVERY_NTH_FRAME != 0:
				continue
			
			new_width = int(img_orig.width/4.0)
			new_height = int(img_orig.height/4.0)
			
			img_small = cv.CreateImage((new_width, new_height), cv.IPL_DEPTH_8U, 3)
			cv.Resize(img_orig, img_small, cv.CV_INTER_AREA)
			
			if DEBUG:
				cv.ShowImage("win", img_small)
			
			img = cv.CreateImage((new_width, new_height), cv.IPL_DEPTH_8U, 3)
			cv.CvtColor(img_small, img, cv.CV_BGR2HLS)
			
			# convert to numpy array
			a = numpy.asarray(cv.GetMat(img))
			a = a.reshape(a.shape[0] * a.shape[1], a.shape[2]) # make it 1-dimensional
			
			# set initial centroids
			init_cluster = []
			for y in [int(new_height/4.0), int(new_height*3/4.0)]:
				for x in [int(new_width*f) for f in [0.25, 0.75]]:
					init_cluster.append(a[y * new_width + x])
			init_cluster.insert(2, a[int(new_height/2.0) * new_width + int(new_width/2.0)])
			
			centroids, labels = scipy.cluster.vq.kmeans2(a, numpy.array(init_cluster))
			
			vecs, dist = scipy.cluster.vq.vq(a, centroids) # assign codes
			counts, bins = scipy.histogram(vecs, len(centroids)) # count occurrences
			centroid_count = []
			for i, count in enumerate(counts):
				#print centroids[i], count
				if count > 0:
					centroid_count.append((centroids[i].tolist(), count))
			
			#centroids = centroids.tolist()
			#centroids.sort(hls_sort)
			
			centroid_count.sort(hls_sort2)
			
			px_count = new_width * new_height
			x = 0
			for item in centroid_count:
				count = item[1] * (PIXELS_PER_COLOR*NUM_CLUSTERS)
				count = int(math.ceil(count / float(px_count)))
				centroid = item[0]
				for l in range(count):
					if x+l >= PIXELS_PER_COLOR*NUM_CLUSTERS:
						break
					cv.Set2D(output_img, frame_counter, x+l, (centroid[0], centroid[1], centroid[2]))
				x += count
			
			if DEBUG:
				if cv.WaitKey(1) == 27:
					cv.DestroyWindow("win");
					return
			
			frame_counter += 1
		
		output_img_rgb = cv.CreateImage(cv.GetSize(output_img), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(output_img, output_img_rgb, cv.CV_HLS2BGR)
		cv.SaveImage(OUTPUT_DIR_NAME + "\\shot_colors_%04d.png" % (scene_nr), output_img_rgb)
	
	if DEBUG:
		cv.DestroyWindow("win");
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return



# #########################
if __name__ == "__main__":
	main()
# #########################
