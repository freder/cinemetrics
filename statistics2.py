# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as et
import subprocess


def get_fps(video_path):
	"""
	ID_VIDEO_WIDTH=716
	ID_VIDEO_HEIGHT=424
	ID_VIDEO_FPS=25.000
	ID_VIDEO_ASPECT=2.4017
	ID_START_TIME=0.00
	ID_LENGTH=6312.09
	"""
	popen = subprocess.Popen("D:\\archiv\\software\\tools\\MPlayer-rtm-svn-32848\\mplayer.exe -vo null -ao null -frames 0 -identify \"%s\"" % video_path, stdout=subprocess.PIPE)
	output = popen.stdout
	# ID_VIDEO_FPS=25.000
	fps = None
	#length = None
	for line in output:
		if line.startswith("ID_VIDEO_FPS="):
			fps = line[line.index("=")+1:]
			fps = float(fps)
	#		print "FRAME RATE:", fps
		
	#	if line.startswith("ID_LENGTH="):
	#		length = line[line.index("=")+1:]
	#		length = float(length)
	#		print "LENGTH:", length
	return fps


def main():
	os.chdir(sys.argv[1])
	
	tree = et.parse("project.xml")
	
	movie = tree.getroot()
	
	frames = int( movie.attrib["frames"] )
	print "frames:\t%d" % frames
	
	fps = get_fps(movie.attrib["path"])
	print "fps:\t%.2f" % fps
	
	minutes = float(frames)/(fps*60)
	print "dur:\t%.2f min (%.1f percent of 2 h)" % (minutes, 100*minutes/120)
	
	f = open("shots.txt", "r")
	lines = [line for line in f if line]
	f.close()
	scene_longest = 0
	scene_shortest = frames
	for line in lines:
		length = int( line.split("\t")[2] )
		if length > scene_longest:
			scene_longest = length
		if length < scene_shortest:
			scene_shortest = length
	scene_count = len( lines )
	
	print ""
	print "scenes:\t%d" % scene_count
	print "avg shot dur:\t%.2f s" % (60*minutes/scene_count)
	print "longest shot:\t%.2f s" % (scene_longest/fps)
	print "shortest shot:\t%.2f s" % (float(scene_shortest)/fps)
	
	# words per second
	file = open("subtitles.txt")
	s = file.read()
	file.close()
	word_count = len( s.split() )
	words_per_second = (word_count/(frames/fps))
	print ""
	print "avg words per second:\t%.2f (%.1f percent of the average)" % (words_per_second, words_per_second * 100)
	print "avg words per minute:\t%.2f" % (words_per_second * 60)
	
	raw_input("- done -")
	return
	

# #########################
if __name__ == "__main__":
	main()
# #########################
