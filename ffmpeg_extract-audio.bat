REM ffmpeg -i bond.vob -f mp3 -ar 44100 -ab 128000 -ac 2 audio.mp3
ffmpeg -i %1 -f wav -ac 1 -ar 16000 audio.wav
