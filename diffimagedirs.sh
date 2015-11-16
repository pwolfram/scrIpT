#!/bin/bash
DIR1=$1
DIR2=$2
EXT=$3
OUTPUTDIR=$4
# make the outputdir if it doesn't exist
if [ ! -d $OUTPUTDIR ];  then
  echo 'Making directory' $OUTPUTDIR;
  mkdir $OUTPUTDIR;
fi
# write log to file
logfile=$OUTPUTDIR/diffimage.log
exec > $logfile 2>&1

# assume files same in each folder
for fname in ./{$DIR1,$DIR2}/*.$EXT; do 
  proceed=true
  # strip the folder from this
  fname=`basename $fname`
  if [ ! -e $DIR2/$fname ]; then 
    # give warning 
    echo $DIR2 " didn't have the file " $DIR2/$fname ' not diffing it...'
    proceed=false
  fi
  if [ ! -e $DIR1/$fname ]; then 
    # give warning
    echo $DIR1 " didn't have the file " $DIR1/$fname ' not diffing it...'
    proceed=false
  fi
  # if both have the file proceed
  if $proceed; then
    echo 'diffing files ' $DIR1/$fname ' and ' $DIR2/$fname 
    # combine them and annotate them
    text1="text 100,75 '"$DIR1/$fname"'"
    text2="text 100,75 '"$DIR2/$fname"'"
    echo $text1
    convert $DIR1/$fname -fill black -pointsize 15 -draw "$text1" /tmp/1$fname
    convert $DIR2/$fname -fill black -pointsize 15 -draw "$text2" /tmp/2$fname
    montage -mode concatenate -tile x1 /tmp/1$fname /tmp/2$fname $OUTPUTDIR/labeled_$fname
    montage -mode concatenate -tile x1 $DIR1/$fname $DIR2/$fname $OUTPUTDIR/$fname
    compare $DIR1/$fname $DIR2/$fname $OUTPUTDIR/diff_compare_$fname
    composite $DIR1/$fname $DIR2/$fname -compose difference $OUTPUTDIR/diff_composite_$fname
    convert $OUTPUTDIR/diff_composite_$fname -auto-level $OUTPUTDIR/diff_composite_norm_$fname
    convert -delay 50 /tmp/1$fname /tmp/2$fname -loop 0 $OUTPUTDIR/diff_animated_$fname.gif
  fi
done

