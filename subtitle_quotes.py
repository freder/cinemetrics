# -*- coding: utf-8 -*-
import sys
import os
from pysrt import SubRipFile, SubRipItem, SubRipTime
from lxml import etree
import re
import string
import xml.etree.ElementTree as et


from lib import timecode_to_seconds, seconds_to_timecode


QUOTE_MIN_LEN = 5
QUOTE_MAX_LEN = 300


def main():
	os.chdir(sys.argv[1])
	
	raw_input("are the subtitle timings correct?".upper())
	
	# ##### extract quotes from IMDB html-file ###################################################
	f = open(r"quotes.htm", "r")
	parser = etree.HTMLParser()
	tree = etree.parse(f, parser)
	f.close()
	root = tree.getroot()

	quotes = []
	for div in root.xpath("//div"):
		try:
			c = div.attrib["class"]
			if c == "sodatext":
				s = etree.tostring(div)
				s = re.sub("\<div.*\>\n", "", s)
				s = re.sub("\</div.*\>", "", s)
				
				#s = re.sub("\<b\>.*\</b\>:\n", "- ", s) # names
				s = re.sub("\<b\>\<a.*\"\>", "", s)
				s = re.sub("\</a\>\</b\>:\n", ": ", s)
				
				# share this quote
				s = re.sub("\<p.*\>.*\</p\>", "", s)
				s = re.sub("\<span.*\>.*\</span\>", "", s)
				
				s = re.sub("\[.*\]", "", s) # stage directions
				s = re.sub("\<br/\>", "", s)
				s = re.sub("  ", " ", s)
				lines = [line.strip() for line in s.split("\n")]
				lines = [line for line in lines if len(line) > 0]
				if len(lines) == 1:
					lines[0] = lines[0][1:].strip()
				quote = "\n".join(lines)
				# #######
				'''if len(quote) >= QUOTE_MIN_LEN and len(quote) <= QUOTE_MAX_LEN:
					quotes.append(quote)'''
				quotes.append(quote)
				# #######
		except:
			continue
	
	quotes = list( set(quotes) )
	quotes_clean = [re.sub("[%s]+" % re.escape(string.punctuation), "", x) for x in quotes]
	quotes_clean = [x.lower().strip() for x in quotes_clean]
	"""for quote in quotes_clean:
		print quote, "\n" """
	
	# ##### read subtitles from srt-file ###################################################
	subs = SubRipFile.open('subtitles.srt')
	"""for sub in subs:
		#print sub.from_string()
		print sub.index
		#print sub.shift()
		print sub.start
		print sub.end
		print sub.text
		print "\n" """
	#print dir(subs)
	
	timecode_quote = {}
	for item in subs:
		item.text = re.sub("[%s]+" % re.escape(string.punctuation), "", item.text)
		item.text = item.text.lower().strip()
		text = item.text.split("\n")[0] # first line only
		
		for i, quote in enumerate(quotes_clean):
			if len(text.split(" ")) >= 3 and text in quote: # we'll get a lot of false hits with only one word :/
				if quotes[i] not in timecode_quote.values():
					timecode_quote[str(item.start)] = quotes[i]
	
	# #####  ###################################################
	tree = et.parse("project.xml")
	movie = tree.getroot()
	fps = float( movie.attrib["fps"] )
	frames = float( movie.attrib["frames"] )
	seconds = frames / fps
	#print seconds
	"""start_frame = float( movie.attrib["start_frame"] )
	start_sec = startframe / fps"""
	
	# sort by timecode
	timecodes = timecode_quote.keys()
	timecodes.sort()
	
	f = open("quotes.txt", "w")
	for tc in timecodes:
		#print tc
		print "%.1f" % (100 * timecode_to_seconds(tc) / seconds) + "%", tc
		print timecode_quote[tc]
		print ""
		f.write("%f#%s\n" % (timecode_to_seconds(tc) / seconds, timecode_quote[tc].replace("\n", "#")))
	f.close()
	
	print "<<", len(timecodes), "QUOTES >>"
	
	
	#raw_input("- done -")
	return



# #########################
if __name__ == "__main__":
	main()
# #########################
