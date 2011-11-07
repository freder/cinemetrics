REM -vf cropdetect
ffmpeg -i VTS_01_1.VOB -vf crop=720:462:0:57 -target dvd -acodec copy cropped.vob