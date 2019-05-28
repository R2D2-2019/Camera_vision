#!/bin/bash
for video in * 
do
    if test -f "$video" 
    then
       ffmpeg -framerate 24 -i "$video" -c copy output.mp4
    fi
done
