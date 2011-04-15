# -*- coding: utf-8 -*-
import cv
import math
import os
import sys
import xml.etree.ElementTree as et
import time


# TODO
# - last 499


DEBUG = False
MAX_FRAMES = 5000
WIDTH = 500

OUTPUT_DIR_NAME = "motion"


def main():
	os.chdir(sys.argv[1])
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except OSError:
		pass
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	file_path = movie.attrib["path"]
	
	if DEBUG:
		cv.NamedWindow("win", cv.CV_WINDOW_AUTOSIZE)
		cv.MoveWindow("win", 200, 200)
	
	cap = cv.CreateFileCapture(file_path)
	cv.QueryFrame(cap)
	
	pixel_count = None
	prev_img = None
	
	global_frame_counter = 0
	file_counter = 0
	
	w = None
	h = None
	
	output_img = cv.CreateImage((WIDTH, MAX_FRAMES), cv.IPL_DEPTH_8U, 3)
	
	f = open("shots.txt", "r")
	lines = [line for line in f if line] # (start_frame, end_frame, duration)
	f.close()
	
	f_frm = open("motion.txt", "w")
	f_avg = open("motion_shot-avg.txt", "w")
	motion = []
	
	t = time.time()
	
	for nr, line in enumerate(lines):
		print (nr+1), "/", len(lines)
		
		duration = int( line.split("\t")[2] )
		
		for frame_counter in range(duration):
			img = cv.QueryFrame(cap)
			if not img:
				print nr, frame_counter
				break
			
			if DEBUG:
				cv.ShowImage("win", img)
			
			global_frame_counter += 1
			
			if nr == 0 and frame_counter == 0: # first shot, first frame
				w = img.width
				h = img.height
				pixel_count = float( img.width * img.height )
				prev_img = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
				cv.Zero(prev_img)
			
			diff = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
			cv.AbsDiff(img, prev_img, diff)
			cv.Threshold(diff, diff, 10, 255, cv.CV_THRESH_BINARY)
			d_color = 0
			for i in range(1, 4):
				cv.SetImageCOI(diff, i)
				d_color += cv.CountNonZero(diff) / pixel_count
			d_color = d_color / 3 # 0..1
			#print "%.1f" % (d_color*100), "%"
			
			motion.append(d_color)
			cv.Copy(img, prev_img)
			
			# WRITE TEXT FILE
			f_frm.write("%f\n" % (d_color))
			if frame_counter == duration-1: # last frame of current shot
				motion_value = sum(motion) / len(motion)
				print "average motion:", motion_value
				f_avg.write("%f\t%d\n" % (motion_value, duration))
				motion = []
			
			# WRITE IMAGE
			if frame_counter == 0: # ignore each first frame -- the diff after a hard cut is meaningless
				global_frame_counter -= 1
				continue
			else:
				for i in range(WIDTH):
					value = d_color * 255
					cv.Set2D(output_img, (global_frame_counter-1) % MAX_FRAMES, i, cv.RGB(value, value, value))
			
			if global_frame_counter % MAX_FRAMES == 0:
				cv.SaveImage(OUTPUT_DIR_NAME + "\\motion_%03d.png" % (file_counter), output_img)
				file_counter += 1
			
			if DEBUG:
				if cv.WaitKey(1) == 27:
					break
	
	if global_frame_counter % MAX_FRAMES != 0:
		#cv.SetImageROI(output_img, (0, 0, WIDTH-1, (global_frame_counter % MAX_FRAMES)-1))
		cv.SetImageROI(output_img, (0, 0, WIDTH-1, (global_frame_counter-1) % MAX_FRAMES))
		cv.SaveImage(OUTPUT_DIR_NAME + "\\motion_%03d.png" % (file_counter), output_img)
	
	f_frm.close()
	f_avg.close()
	
	if DEBUG:
		cv.DestroyWindow("win");
	
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return



# #########################
if __name__ == "__main__":
	main()
# #########################
