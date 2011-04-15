# -*- coding: utf-8 -*-
import cv
import sys
import os
import os.path


OUTPUT_DIR_NAME = "stills_slitscan"


def main():
	os.chdir(sys.argv[1])
	
	try:
		os.mkdir(OUTPUT_DIR_NAME)
	except:
		pass
	
	os.chdir("stills")
	files = [file for file in os.listdir(os.getcwd()) if not os.path.isdir(file)]
	
	width = None
	height = None
	output_img = None
	
	for i, file in enumerate( files ):		
		img = cv.LoadImageM(file)
		
		if i % 100:
			print i, "/", len(files)
		
		if i == 0:
			width = img.width
			height = img.height
			output_img = cv.CreateImage((width, len(files)), cv.IPL_DEPTH_8U, 3)
		
		row = cv.GetRow(img, int( (i/len(files))*height ))
		for x in range(width):
			color = cv.Get1D(row, x)
			cv.Set2D(output_img, i, x, color)
		
	cv.SaveImage("..\\" + OUTPUT_DIR_NAME + "\\still_slitscan.png", output_img)
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
