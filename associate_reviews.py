import json
import sys

TOTAL_ARGS = 2
FILENAME_ARG = 1


def main():
    if len(sys.argv) != TOTAL_ARGS:
        print('usage: python associate_reviews.py <filename>')
        exit(1)

    # All infiles must be in `yelp_academic_dataset/reviews_raw/<filename>`:
    review_dataset = 'yelp_academic_dataset/reviews_raw/' + sys.argv[FILENAME_ARG]
    # All outfiles will be placed in `yelp_academic_dataset/reviews_associated/<filename>`:
    review_associations_dataset = 'yelp_academic_dataset/reviews_associated/' + sys.argv[FILENAME_ARG]
    revs = []

    # Extract review ID, text from JSON file.
    with open(review_dataset, 'r') as infile:
        for line in infile:
            review = json.loads(line)

            review_id = review['review_id']
            business_id = review['business_id']
            rev = {
                'review_id': review_id,
                'business_id': business_id
            }

            revs.append(rev)


    # Save text and parser representations to JSON file.
    for rev in revs:
        with open(review_associations_dataset, 'a') as outfile:
            outfile.write('\n')
            json.dump(rev, outfile)


if __name__ == '__main__':
    main()
