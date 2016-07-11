#!/usr/bin/env bash

if [ $# -eq 1 ] ; then
  # compute runtime hours
  hrs=`printf "%02d" $1`
  echo "Runtime hrs: "$hrs
else
  echo "Wrong arguments supplied, need queue time in hrs"
  exit 1
fi

# get runscript name
path=`pwd`
dir=`basename $path`
runscript=$dir'.run'
echo $runscript

cp $runscript $runscript'.backup'

# add email to run script
perl -i -p0e 's/#PBS  -m ae /"#PBS  -m abe \n#PBS -M phillipwolfram\@gmail.com"/se' $runscript

# modify runtime hrs
sed -i "s/#PBS\s*-l\s*walltime=..:00:00/#PBS  -l walltime=$hrs:00:00/g" $runscript
