# -*- coding: utf-8 -*-
import cv
import numpy
import scipy.cluster
import os
import os.path
import sys
import math

from lib import hls_sort2


DEBUG = False

NUM_CLUSTERS = 5
PIXELS_PER_COLOR = 40
OUTPUT_DIR_NAME = "shot_colors"


def main():
	os.chdir(sys.argv[1])
	output_dir = os.path.join(OUTPUT_DIR_NAME, OUTPUT_DIR_NAME)
	try:
		os.mkdir(output_dir)
	except:
		pass
	
	os.chdir(OUTPUT_DIR_NAME)
	for file in os.listdir(os.getcwd()):
		if os.path.isdir(file):
			continue
		
		img_orig = cv.LoadImageM(file)
		w, h = img_orig.cols, img_orig.rows
		
		img_hls = cv.CreateImage((w, h), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(img_orig, img_hls, cv.CV_BGR2HLS)
		
		output_img = cv.CreateImage((PIXELS_PER_COLOR*NUM_CLUSTERS, h), cv.IPL_DEPTH_8U, 3)
		
		# convert to numpy array
		a = numpy.asarray(cv.GetMat(img_hls))
		a = a.reshape(a.shape[0] * a.shape[1], a.shape[2]) # make it 1-dimensional
		
		# set initial centroids
		init_cluster = []
		step = w / NUM_CLUSTERS
		for x, y in [(0*step, h*0.1), (1*step, h*0.3), (2*step, h*0.5), (3*step, h*0.7), (4*step, h*0.9)]:
			x = int(x)
			y = int(y)
			init_cluster.append(a[y*w + x])
		
		centroids, labels = scipy.cluster.vq.kmeans2(a, numpy.array(init_cluster))
		
		vecs, dist = scipy.cluster.vq.vq(a, centroids) # assign codes
		counts, bins = scipy.histogram(vecs, len(centroids)) # count occurrences
		centroid_count = []
		for i, count in enumerate(counts):
			if count > 0:
				centroid_count.append((centroids[i].tolist(), count))
		
		#centroids = centroids.tolist()
		#centroids.sort(hls_sort)
		
		centroid_count.sort(hls_sort2)
		
		px_count = w * h
		x = 0
		for item in centroid_count:
			count = item[1] * (PIXELS_PER_COLOR*NUM_CLUSTERS)
			count = int(math.ceil(count / float(px_count)))
			centroid = item[0]
			for l in range(count):
				if x+l >= PIXELS_PER_COLOR*NUM_CLUSTERS:
					break
				for y in range(h):
					cv.Set2D(output_img, y, x+l, (centroid[0], centroid[1], centroid[2]))
			x += count
		
		#for centroid_nr, centroid in enumerate(centroids):
		#	for j in range(PIXELS_PER_COLOR):
		#		x = centroid_nr*PIXELS_PER_COLOR + j
		#		for y in range(h):
		#			cv.Set2D(output_img, y, x, (centroid[0], centroid[1], centroid[2]))
		
		output_img_rgb = cv.CreateImage(cv.GetSize(output_img), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(output_img, output_img_rgb, cv.CV_HLS2BGR)
		cv.SaveImage(os.path.join(OUTPUT_DIR_NAME, file), output_img_rgb)
	
	print "appending..."
	os.chdir(OUTPUT_DIR_NAME)
	os.system("convert shot_colors_*.png -append result.png")
	
	#raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
