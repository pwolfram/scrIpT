#!/bin/bash
DIR1=../CDlaxWendroffSWEz0.00025WorkingWellFullRecordFineRes/movieframes
DIR2=../TVDVanLeerSWEz0.00025WorkingWellFullRecordFineRes/movieframes
NUMFRAMES=0680

for i in $(seq -w 1 $NUMFRAMES); do 
  # combine them and annotate them
  montage -mode concatenate -tile x1 $DIR1/*Visit$i.jpg $DIR2/*Visit$i.jpg $i.jpg; 
  convert $i.jpg -fill white -pointsize 50 -draw "text 212,1388 'a) CD-LaxWendroff'" $i.jpg; 
  convert $i.jpg -fill white -pointsize 50 -draw "text 2508,1388 'b) TVD-VanLeer'" $i.jpg; 
done


