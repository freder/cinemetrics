# -*- coding: utf-8 -*-
import sys
import cv
import time
import winsound
import win32api, win32con
import os.path
import xml.etree.ElementTree as et


DEBUG = False
#DEBUG = True
DEBUG_INTERACTIVE = False

OUTPUT_DIR_NAME = "shot_snapshots"
soundfile = "ton.wav"


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
	
	if DEBUG:
		cv.NamedWindow("win", cv.CV_WINDOW_AUTOSIZE)
		cv.MoveWindow("win", 200, 200)

	hist = None
	prev_hist = None
	prev_img = None

	pixel_count = None
	frame_counter = 0

	last_frame_black = False
	black_frame_start = -1

	t = time.time()

	while 1:
		img_orig = cv.QueryFrame(cap)
		
		if not img_orig: # eof
			cv.SaveImage(OUTPUT_DIR_NAME + "\\%06d.png" % (frame_counter-1), prev_img)
			"""movie.set("frames", str(frame_counter))
			tree.write("project.xml")"""
			break
		
		img = cv.CreateImage((int(img_orig.width/4), int(img_orig.height/4)), cv.IPL_DEPTH_8U, 3)
		cv.Resize(img_orig, img, cv.CV_INTER_AREA)
		
		if frame_counter == 0: # erster frame
			cv.SaveImage(OUTPUT_DIR_NAME + "\\%06d.png" % (0), img)
			pixel_count = img.width * img.height
			prev_img = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
			cv.Zero(prev_img)
		
		if DEBUG and frame_counter % 2 == 1:
			cv.ShowImage("win", img)
		
		img_hsv = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
		cv.CvtColor(img, img_hsv, cv.CV_BGR2HSV)
		
		# #####################
		# METHOD #1: find the number of pixels that have (significantly) changed since the last frame
		diff = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
		cv.AbsDiff(img_hsv, prev_img, diff)
		cv.Threshold(diff, diff, 10, 255, cv.CV_THRESH_BINARY)
		d_color = 0
		for i in range(1, 4):
			cv.SetImageCOI(diff, i)
			d_color += float(cv.CountNonZero(diff)) / float(pixel_count)
		d_color = float(d_color/3.0) # 0..1
		
		# #####################
		# METHOD #2: calculate the amount of change in the histograms
		h_plane = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		s_plane = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		v_plane = cv.CreateMat(img.height, img.width, cv.CV_8UC1)
		cv.Split(img_hsv, h_plane, s_plane, v_plane, None)
		planes = [h_plane, s_plane, v_plane]
		
		hist_size = [50, 50, 50]
		hist_range = [[0, 360], [0, 255], [0, 255]]
		if not hist:
			hist = cv.CreateHist(hist_size, cv.CV_HIST_ARRAY, hist_range, 1)
		cv.CalcHist([cv.GetImage(i) for i in planes], hist)
		cv.NormalizeHist(hist, 1.0)
		
		if not prev_hist:
			prev_hist = cv.CreateHist(hist_size, cv.CV_HIST_ARRAY, hist_range, 1)
			# wieso gibt es kein cv.CopyHist()?!
			cv.CalcHist([cv.GetImage(i) for i in planes], prev_hist)
			cv.NormalizeHist(prev_hist, 1.0)
			continue
		
		d_hist = cv.CompareHist(prev_hist, hist, cv.CV_COMP_INTERSECT)
		
		# combine both methods to make a decision
		if ((0.4*d_color + 0.6*(1-d_hist))) >= 0.48:
			if DEBUG:
				if frame_counter % 2 == 0:
					cv.ShowImage("win", img)
				winsound.PlaySound(soundfile, winsound.SND_FILENAME|winsound.SND_ASYNC)
			print "%.3f" % ((0.4*d_color + 0.6*(1-d_hist))), "%.3f" % (d_color), "%.3f" % (1-d_hist), frame_counter
			if DEBUG and DEBUG_INTERACTIVE:
				if win32api.MessageBox(0, "cut?", "", win32con.MB_YESNO) == 6: #yes
					cv.SaveImage(OUTPUT_DIR_NAME + "\\%06d.png" % (frame_counter), img)
			else:
				cv.SaveImage(OUTPUT_DIR_NAME + "\\%06d.png" % (frame_counter), img)
		
		cv.CalcHist([cv.GetImage(i) for i in planes], prev_hist)
		cv.NormalizeHist(prev_hist, 1.0)
		
		# #####################
		# METHOD #3: detect series of (almost) black frames as an indicator for "fade to black"
		average = cv.Avg(v_plane)[0]
		if average <= 0.6:
			if not last_frame_black: # possible the start
				print "start", frame_counter
				black_frame_start = frame_counter
			last_frame_black = True
		else:
			if last_frame_black: # end of a series of black frames
				cut_at = black_frame_start + int( (frame_counter - black_frame_start) / 2 )
				print "end", frame_counter, "cut at", cut_at
				img_black = cv.CreateImage((img_orig.width/4, img_orig.height/4), cv.IPL_DEPTH_8U, 3)
				cv.Set(img_black, cv.RGB(0, 255, 0))
				cv.SaveImage(OUTPUT_DIR_NAME + "\\%06d.png" % (cut_at), img_black)
			last_frame_black = False
		
		cv.Copy(img_hsv, prev_img)
		frame_counter += 1
		
		if DEBUG:
			if cv.WaitKey(1) == 27:
				break
		

	if DEBUG:
		cv.DestroyWindow("win");
	
	print "%.2f min" % ((time.time()-t) / 60)
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
