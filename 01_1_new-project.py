# -*- coding: utf-8 -*-
import sys
import os
import os.path
import xml.etree.ElementTree as et
import cv

PROJECTS_DIR_NAME = "projects"


def main():
	movie_path, movie_file = os.path.split(sys.argv[1])
	os.chdir(os.path.split(sys.argv[0])[0])
	project_dir = os.path.splitext(movie_file)[0]
	try:
		os.mkdir(os.path.join(PROJECTS_DIR_NAME, project_dir))
	except:
		pass
	
	# generate project xml file:
	root = et.Element("movie")
	#root.set("title", project_dir)
	root.set("path", sys.argv[1])
	#root.set("frames", str(frame_count))
	#root.set("fps", str(fps))
	
	# wrap and save
	tree = et.ElementTree(root)
	os.chdir(os.path.join(PROJECTS_DIR_NAME, project_dir))
	tree.write("project.xml")
	
	print "don't forget to crop / remove any black borders!"
	
	raw_input("- done -")
	return


# #########################
if __name__ == "__main__":
	main()
# #########################