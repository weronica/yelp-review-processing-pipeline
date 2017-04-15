#!/bin/csh

#$ -o process_reviews.out
#$ -e process_reviews.err
#$ -l 'arch=*64*'
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -m eas
#$ -pe parallel-onenode 4

# set terminal
export TERM=vt100

# when I start running
echo "Start - "
/bin/date

# activate virtualenv
source ../ENV/bin/activate

# run script
python process_reviews.py $1

# when I am finished
echo "Finish - "
/bin/date
