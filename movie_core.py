# -*- coding: utf-8 -*-
import cv
import sys
import os
import os.path
import math
import xml.etree.ElementTree as et
import time


OUTPUT_DIR_NAME = "core"


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
	
	# skip frames in the beginning, if neccessary
	start_frame = int( movie.attrib["start_frame"] )
	for i in range(start_frame):
		cv.QueryFrame(cap)
	
	f = open("scenes.txt", "r")
	lines = [line for line in f if line]
	f.close()
	
	w = None
	h = None
	radius = None
	umfang = None
	
	t = time.time()
	
	for nr, line in enumerate(lines):
		print (nr+1), "/", len(lines)
		
		width = int( line.split("\t")[2] )
		
		output_img = None
		
		for frame_counter in range(width):			
			img = cv.QueryFrame(cap)
			if not img:
				break
			
			if nr == 0:
				w = img.width
				h = img.height
				radius = int( (0.9 * h) / 2 )
				umfang = int( 2 * math.pi * radius )
			
			if frame_counter == 0:
				output_img = cv.CreateImage((umfang, width), cv.IPL_DEPTH_8U, 3)
				cv.SaveImage(os.path.join(OUTPUT_DIR_NAME, "core_%04d_a.png" % nr), img)
			elif frame_counter == width-1:
				cv.SaveImage(os.path.join(OUTPUT_DIR_NAME, "core_%04d_b.png" % nr), img)
			
			for i in range(umfang):
				alpha = math.radians( i * (360.0 / umfang) )
				x = (w / 2) + math.sin(alpha) * radius
				y = (h / 2) + math.cos(alpha) * radius
				px = cv.Get2D(img, int(y), int(x))
				cv.Set2D(output_img, frame_counter, i, px)
		
		cv.SaveImage(os.path.join(OUTPUT_DIR_NAME, "core_%04d.png" % nr), output_img)
	
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
