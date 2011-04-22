# -*- coding: utf-8 -*-
import cv
import math
import os
import sys
import xml.etree.ElementTree as et
import time


OUTPUT_DIR_NAME = "shot_slitscans"


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except OSError:
		pass
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	file_path = movie.attrib["path"]
	
	cap = cv.CreateFileCapture(file_path)
	cv.QueryFrame(cap)
	
	# skip frames in the beginning, if neccessary
	start_frame = int( movie.attrib["start_frame"] )
	for i in range(start_frame):
		cv.QueryFrame(cap)
	
	f = open("shots.txt", "r")
	lines = [line for line in f if line]
	f.close()
	
	t = time.time()
	
	w = None
	h = None
	
	#for line in f:
	for nr, line in enumerate(lines):
		print (nr+1), "/", len(lines)
		
		#frame_from, frame_to, width, scene_nr = [int(i) for i in line.split("\t")]
		#width, scene_nr = [int(i) for i in line.split("\t")][2:]
		start_frame, end_frame, width = [int(splt) for splt in line.split("\t")]
		#width *= STRETCH_FAKTOR
		
		faktor = None
		output_img = None
		
		for frame_counter in range(width):
			#if frame_counter % STRETCH_FAKTOR == 0:
			#	img = cv.QueryFrame(cap)
			#	if not img:
			#		break
			
			img = cv.QueryFrame(cap)
			if not img:
				break
			
			if nr == 0:
				w = img.width
				h = img.height
				
			if frame_counter == 0:
				faktor = float(w) / float(width)
				output_img = cv.CreateImage((width, h), cv.IPL_DEPTH_8U, 3)
			
			col_nr = faktor * (frame_counter+0.5)
			col_nr = int( math.floor(col_nr) )
			#print frame_counter, width, col_nr, w
			col = cv.GetCol(img, col_nr)
			
			for i in range(h):
				cv.Set2D(output_img, i, frame_counter, cv.Get1D(col, i))
			
		#return
			
		cv.SaveImage(OUTPUT_DIR_NAME + "\\shot_slitscan_%03d_%d.png" % (nr+1, start_frame), output_img)
	
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return
	

# #########################
if __name__ == "__main__":
	#STRETCH_FAKTOR = 1
	main()
# #########################
