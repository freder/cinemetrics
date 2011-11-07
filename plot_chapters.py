# -*- coding: utf-8 -*-
import sys
import os
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import math
import numpy


os.chdir(sys.argv[1])

# ===== SHOTS ==================================================================================================
f = open("chapters.txt", "r")
values = [int(value) for value in f if value]
f.close()

fig = plt.figure()
ax = fig.add_subplot(111)

#last_endframe = 0
tree = et.parse("project.xml")
movie = tree.getroot()
last_endframe = int( movie.attrib["start_frame"] )

for i, item in enumerate(values):
	y = 1
	if (i % 2 == 0):
		y = 2
	ax.hlines(y, last_endframe, item, lw=30)
	last_endframe = item

ax.axis("off")
plt.show()