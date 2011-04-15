# -*- coding: utf-8 -*-
import cv
import os
import os.path
import sys


def main():
	os.chdir(os.path.join(sys.argv[1], "motion"))
	try:
		os.mkdir("klein")
	except OSError:
		pass
	
	#os.system("del klein\\*.png")
	os.system("convert motion_*.png -adaptive-resize 500x500! klein\\motion_%02d.png")
	
	os.chdir("klein")
	os.system("convert motion_*.png -append result.png")
	
	img = cv.LoadImageM("result.png")
	values = []
	
	for y in range(img.rows):
		value = cv.Get1D( cv.GetRow(img, y), 0)[0]
		values.append(value)
	
	values.sort(reverse=True)
	
	output_img = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
	for y in range(img.rows):
		for x in range(img.cols):
			cv.Set2D(output_img, y, x, cv.RGB(values[y], values[y], values[y]))
	
	cv.SaveImage("result_sorted.png", output_img)
	
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################