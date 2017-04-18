import json
from os import listdir
from os.path import isfile, join
import sys


def main():
    review_path = 'yelp_academic_dataset/reviews_parsed/'
    review_files = [f for f in listdir(review_path) if isfile(join(review_path, f))]

    num_words = 0
    num_reviews = 0
    for review_file in review_files:
        # Extract review ID, text from JSON file.
        with open(review_path + review_file, 'r') as infile:
            print('%s started' % review_file)

            next(infile)
            for line in infile:
                review = json.loads(line)

                num_words += len(review['text'].split(' '))
                print num_words
                num_reviews += 1

    print('total number of words: %d' % num_words)
    print('total number of reviews: %d' % num_reviews)
    print('total number of reviews: %f' % num_words / float(num_reviews))


if __name__ == '__main__':
    main()
