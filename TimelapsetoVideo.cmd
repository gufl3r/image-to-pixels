@echo off
set /p Input=Enter images path prefix: 
set "Path=%Input%%%d.jpg"
.\ffmpeg.exe -r 60 -i "%Path%" -b:v 40096k -maxrate:v 50096k -minrate:v 0 -bufsize 50096k .\output\a.avi
pause