#!/bin/bash

for filename in ./yelp_academic_dataset/reviews_raw/*; do
    if [ -f "./yelp_academic_dataset/reviews_parsed/$(basename $filename)" ];
    then
      echo "skipping $(basename "$filename")...\n"
    else
      echo "queueing $(basename "$filename")..."
      qsub parse_reviews.sh $(basename "$filename") -nlp
    fi
done
