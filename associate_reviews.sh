#!/bin/csh

#$ -o associate_reviews.out
#$ -e associate_reviews.err
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
python associate_reviews.py $1

# when I am finished
echo "Finish - "
/bin/date
