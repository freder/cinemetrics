# -*- coding: utf-8 -*-
import sys
import os
import os.path
import glob
import cv
import math
import numpy
import scipy.cluster


from lib import hls_sort2


OUTPUT_DIR_NAME = "chapters"

def main():
	os.chdir(sys.argv[1])
	
	f_shots = open("shots.txt")
	shots = [(int(start), int(end)) for start, end in [line.split("\t")[0:2] for line in f_shots if line]]
	f_shots.close()
	
	f_chapters = open("chapters.txt")
	chapters = [int(line) for line in f_chapters]
	f_chapters.close()
	
	os.chdir("shot_colors")
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except:
		pass
	
	filenames = glob.glob("shot_colors_*.png")
	
	frm = 0
	ch = 1
	for i, shot in enumerate(shots):
		if ch == len(chapters):
			print "den rest noch"
			print " ".join(filenames[frm:])
			os.system("convert %s -append chapters\\%02d.png" % (" ".join(filenames[frm:]), ch))
			break
		elif shot[1] > chapters[ch]:
			print ch, ":", frm, "->", i-1
			print " ".join(filenames[frm:i])
			os.system("convert %s -append chapters\\%02d.png" % (" ".join(filenames[frm:i]), ch))
			frm = i
			ch += 1
	
	os.chdir(OUTPUT_DIR_NAME)
	NUM_CLUSTERS = 5
	PIXELS_PER_COLOR = 40
	
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
		
		output_img_rgb = cv.CreateImage(cv.GetSize(output_img), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(output_img, output_img_rgb, cv.CV_HLS2BGR)
		cv.SaveImage(file, output_img_rgb)
	
	os.system("convert *.png -append _CHAPTERS.png")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################