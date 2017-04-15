#!/bin/bash

for filename in ./yelp_academic_dataset/reviews_parsed/*; do
    if [ -f "./yelp_academic_dataset/reviews_processed/$(basename $filename)" ];
    then
      echo "skipping $(basename "$filename")...\n"
    else
      echo "queueing $(basename "$filename")..."
      qsub process_reviews.sh $(basename "$filename")
    fi
done
