# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as et


def main():
	os.chdir(sys.argv[1])
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	duration = int( movie.attrib["frames"] )
	start_frame = int( movie.attrib["start_frame"] )
	end_frame = int( movie.attrib["end_frame"] )
	
	f = open("chapters.txt~", "r")
	chapters = [int(frame) for frame in f if frame]
	f.close()
	
	chapters = [ch for ch in chapters if ch < end_frame and ch > start_frame] # get rid of things that are outside of the bounds
	chapters = [start_frame] + chapters
	#chapters[0] = start_frame  # in case we removed some credits from the beginning
	chapters.append(end_frame) # so that we know how long the last chapter is
	
	dur_counter = 0
	for i in range( len(chapters) - 1 ):
		dur_counter += chapters[i+1] - chapters[i]
	
	print duration
	print dur_counter
	
	f_out = open("chapters.txt", "w")
	for ch in chapters:
		f_out.write("%d\n" % (ch))
	f_out.close()
	
	return


# #########################
if __name__ == "__main__":
	main()
# #########################