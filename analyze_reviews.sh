#!/bin/csh

#$ -o analyze_reviews.out
#$ -e analyze_reviews.err
#$ -l 'arch=*64*'
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -M whartonv@seas.upenn.edu
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
python analyze_reviews.py

# when I am finished
echo "Finish - "
/bin/date
