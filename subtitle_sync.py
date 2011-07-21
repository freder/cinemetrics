import math
import pysrt


from lib import timecode_to_seconds, seconds_to_timecode
	

#def corrected_seconds(s, speed, offset):
#	return (s / speed) + offset


PROJECT = "Annie Hall"
	
	
def main():
	tc_1 = timecode_to_seconds("00:00:53,840")
	tc_1_real = timecode_to_seconds("00:00:49,000")
	
	tc_2 = timecode_to_seconds("01:27:22,640")
	tc_2_real = timecode_to_seconds("01:27:18,000")
	
	speed = (tc_1 - tc_2) / (tc_1_real - tc_2_real)
	#print speed
	offset =  tc_1_real - (tc_1 / speed)
	#print offset
	#print (tc_1 / speed) + offset, tc_1_real
	
	#print "00:00:59,225"
	#print seconds_to_timecode(timecode_to_seconds("00:00:59,225"))
	
	#print corrected_seconds(tc_1, speed, offset), seconds_to_timecode(corrected_seconds(tc_1, speed, offset))
	file_orig = pysrt.SubRipFile.open("projects\\" + PROJECT + "\\subtitles.srt~")
	
	for sub in file_orig:
		sub.start = timecode_to_seconds(str(sub.start))
		sub.start = (sub.start / speed) + offset
		sub.start = seconds_to_timecode(sub.start)
		
		sub.end = timecode_to_seconds(str(sub.end))
		sub.end = (sub.end / speed) + offset
		sub.end = seconds_to_timecode(sub.end)
	
	file_orig.save("projects\\" + PROJECT + "\\subtitles.srt", "utf-8") # , "utf-8", "\n"


# #########################
if __name__ == "__main__":
	main()
# #########################