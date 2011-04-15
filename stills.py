# -*- coding: utf-8 -*-
import cv
import math
import os
import sys
import xml.etree.ElementTree as et
import time


EVERY_NTH_FRAME = 50


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir("stills")
	except OSError:
		pass
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	file_path = movie.attrib["path"]
	
	cap = cv.CreateFileCapture(file_path)
	frame_counter = 0
	
	t = time.time()
	
	while 1:
		img = cv.QueryFrame(cap)
		if not img:
			break
		
		cv.SaveImage("stills\\still_%07d.jpg" % (frame_counter), img)
		frame_counter += 1
		
		for i in range(EVERY_NTH_FRAME-1):
			cv.GrabFrame(cap)
			frame_counter += 1
	
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
