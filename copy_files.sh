#!/usr/bin/env bash
#SBATCH --workdir ./
#SBATCH --account=w17_mpasles
#SBATCH --nodes=120
#SBATCH --ntasks-per-node=36
#SBATCH --job-name copy_files
#SBATCH --time=0:10:00

echo 'Started on '`date`

module purge
module load gcc openmpi

jobid=$SLURM_JOB_ID

# get files with environments for each node
rm -rf sadc_outfile
mpirun --map-by ppr:1:node -mca btl tcp,self --output-filename sadc_outfile /bin/bash -c "/bin/env "

# filter nodes to get hostnames
grep SLURMD_NODENAME sadc_outfile.1.* | sed 's/.*=//g' | sort > hostnames.txt
rm -rf sadc_outfile*

# this is the list of hostnames
cat hostnames.txt

archiveloc='/lustre/scratch3/turquoise/pwolfram/ZISO_5km_particle_files/'
mkdir -p archiveloc

i=0
for host in `cat hostnames.txt`; do
  if [ $i -lt $SLURM_NNODES ]; then

    file=`sed -n "$((i+1))p" analysis_files.txt` 
    echo $file

    folder=$archiveloc/`dirname ${file}`
    echo $folder
    mkdir -p ${folder}
   
    echo 'Launching job on node '$host' for iterate '$i' output in file output'$i'-'$host'-'$jobid'.txt for '\
      $folder
    mpirun -np 1 --map-by ppr:1:node -host $host \
      cp $file $folder/`basename $file` \
      &> file_cp_output"$i"-"$host"-"$jobid".txt &

    let i++
  fi
done
wait

rm hostnames.txt

echo 'Finished on '`date`
