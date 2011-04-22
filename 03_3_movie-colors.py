# -*- coding: utf-8 -*-
import cv
import os
import os.path
import sys
import numpy
import scipy
import scipy.cluster
import math

#from lib import hls_sort


from colormath.color_objects import HSLColor, RGBColor
def difference(a, b): # HLS
	print a, b
	#c1 = HSLColor(hsl_h = a[0], hsl_s = a[2]/100.0, hsl_l = a[1]/100.0)
	#c2 = HSLColor(hsl_h = b[0], hsl_s = a[2]/100.0, hsl_l = a[1]/100.0)
	c1 = RGBColor(a[0], a[1], a[2])
	c2 = RGBColor(b[0], b[1], b[2])
	#c1.convert_to('lab')
	#c2.convert_to('lab')
	print c1.delta_e(c2)
	return c1.delta_e(c2)


#import grapefruit
#def difference(a, b):
#	c1 = grapefruit.Color.NewFromHsl(a[0], a[2], a[1])
#	c2 = grapefruit.Color.NewFromHsl(b[0], b[2], b[1])
#	return 1


def sort_by_distance(colors):
	# Find the darkest color in the list.
	root = colors[0]
	for color in colors[1:]:
		if color[1] < root[1]: # l
			root = color
	
	# Remove the darkest color from the stack,
	# put it in the sorted list as starting element.
	stack = [color for color in colors]
	stack.remove(root)
	sorted = [root]
	
	# Now find the color in the stack closest to that color.
	# Take this color from the stack and add it to the sorted list.
	# Now find the color closest to that color, etc.
	while len(stack) > 1:
		closest, distance = stack[0], difference(stack[0], sorted[-1])
		for clr in stack[1:]:
			d = difference(clr, sorted[-1])
			if d < distance:
				closest, distance = clr, d
		stack.remove(closest)
		sorted.append(closest)
	sorted.append(stack[0])
	
	return sorted


WIDTH = 1000
OUTPUT_DIR_NAME = "shot_colors"


def main():
	project_root_dir = sys.argv[1]
	os.chdir(project_root_dir)
	os.chdir(os.path.join(OUTPUT_DIR_NAME, OUTPUT_DIR_NAME))
	
	output_img = cv.CreateImage((WIDTH, WIDTH), cv.IPL_DEPTH_8U, 3)
	
	print os.system("identify -format \"%k\" result.png")
	print "reducing colors to 10"
	os.system("convert result.png +dither -colors 10 result_quant.png")
	
	img_orig = cv.LoadImageM("result_quant.png")
	output_img = cv.CreateImage((WIDTH, WIDTH), cv.IPL_DEPTH_8U, 3)
	
	img_hls = cv.CreateImage(cv.GetSize(img_orig), cv.IPL_DEPTH_8U, 3)
	cv.CvtColor(img_orig, img_hls, cv.CV_BGR2HLS)
	
	pixels = numpy.asarray(cv.GetMat(img_hls))
	d = {}
	
	print "counting..."
	for line in pixels:
		for px in line:
			if tuple(px) in d:
				d[tuple(px)] += 1
			else:
				d[tuple(px)] = 1
	
	colors = d.keys()
	#print "%d pixels, %d colors" % (img_orig.width*img_orig.height, len(colors))
	
	print "sorting..."
	#colors.sort(hls_sort)
	colors = sort_by_distance(colors)
	
	px_count = img_orig.width * img_orig.height
	x_pos = 0
	
	print "building image..."
	for color in colors:
		l = d[color] / float(px_count)
		l = int(math.ceil( l*WIDTH ))
		
		for x in range(l):
			if x_pos+x >= WIDTH:
					break
			for y in range(WIDTH):
				cv.Set2D(output_img, y, x_pos+x, (int(color[0]), int(color[1]), int(color[2])))
		x_pos += l
	
	print "saving..."
	output_img_rgb = cv.CreateImage(cv.GetSize(output_img), cv.IPL_DEPTH_8U, 3)
	cv.CvtColor(output_img, output_img_rgb, cv.CV_HLS2BGR)
	cv.SaveImage("_RESULT.png", output_img_rgb)
	
	os.chdir( r"..\.." )
	f = open("colors.txt", "w")
	row = cv.GetRow(output_img_rgb, 0)
	
	counter = 0
	last_px = cv.Get1D(row, 0)
	for i in range(WIDTH):
		px = cv.Get1D(row, i)
		if px == last_px:
			counter += 1
			if i == WIDTH-1:
				f.write("%d, %d, %d, %d\n" % (int(last_px[2]), int(last_px[1]), int(last_px[0]), counter))
			continue
		else:
			f.write("%d, %d, %d, %d\n" % (int(last_px[2]), int(last_px[1]), int(last_px[0]), counter))
			counter = 1
			last_px = px
	f.close()
	
	return


# #########################
if __name__ == "__main__":
	main()
# #########################
