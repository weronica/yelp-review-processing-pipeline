#!/bin/bash

for filename in ./yelp_academic_dataset/reviews_raw/*; do
    if [ -f "./yelp_academic_dataset/reviews_associated/$(basename $filename)" ];
    then
      echo "skipping $(basename "$filename")...\n"
    else
      echo "associating $(basename "$filename")..."
      qsub associate_reviews.sh $(basename "$filename") -nlp
    fi
done
