# -*- coding: utf-8 -*-
import cv
import math
import os
import sys
import xml.etree.ElementTree as et


OUTPUT_DIR = "100_stills"


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir(OUTPUT_DIR)
	except OSError:
		pass
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	file_path = movie.attrib["path"]
	fps = float( movie.attrib["fps"] )
	
	cap = cv.CreateFileCapture(file_path)
	cv.QueryFrame(cap)
	
	# skip frames in the beginning, if neccessary
	start_frame = int( movie.attrib["start_frame"] )
	for i in range(start_frame):
		cv.QueryFrame(cap)
	
	end_frame = int( movie.attrib["end_frame"] )
	every_nth_frame = int( (end_frame - start_frame) / 100 )
	print "every", every_nth_frame, "frames"
	print "=", every_nth_frame / fps, "sec"
	frame = start_frame
	counter = 1
	
	while 1:
		print counter
		img = cv.QueryFrame(cap)
		if not img or frame > end_frame:
			break
		
		cv.SaveImage(OUTPUT_DIR + "\\still_%07d.jpg" % (frame), img)
		
		for i in range(every_nth_frame-1):
			cv.GrabFrame(cap)
		
		frame += every_nth_frame
		counter += 1
	
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
