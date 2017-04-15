# Siftin' Through Yelp Reviews

Pipeline for gettin' some meaningful shtuff from [lots o' Yelp reviews](https://www.yelp.com/dataset_challenge).

Stages:
  1. Parsin'
  2. Associatin'
  3. Processin'
  4. Analyzin'
  5. Comparin'

## Parse

Run the [Stanford Parser](http://nlp.stanford.edu/software/lex-parser.shtml) over all Yelp reviews.

**Warning**: This step takes several days to complete when run on nlpgrid.

```sh
$ ./qsub_all_parse.sh
```

Input:
  - `reviews_raw/*`

Scripts:
  - `parse_reviews.py`
  - `parse_reviews.sh`
  - `qsub_all_parse.sh`

Output:
  - `reviews_parsed/*`

## Associate

Associate each review with its restaurant.

```sh
$ make associate
```

Input:
  - `reviews_raw/*`

Scripts:
  - `associate_reviews.py`
  - `associate_reviews.sh`
  - `qsub_all_associate.sh`

Output:
  - `reviews_associated/*`

## Process

Extract all NNs, JJs, NN+JJ, ADV+JJ pairs from reviews.

```sh
$ ./qsub_all_process.sh
```

Input:
  - `reviews_parsed/*`

Scripts:
  - `process_reviews.py`
  - `process_reviews.sh`
  - `qsub_all_process.sh`

Output:
  - `reviews_processed/*`
  - `reviews_processed_sm/*`

## Analyze

Determine most frequent NNs, JJs, NN+JJ, ADV+JJ pairs across all reviews.

```sh
$ make analyze
```

Input
  - `reviews_processed_sm/*`
  - `intensifiers_20160609_3.json`

Scripts:
  - `analyze_reviews.py`
  - `analyze_reviews.sh`

Output:
  - `reviews_analyzed/jj.json`
  - `reviews_analyzed/nn.json`
  - `reviews_analyzed/jj_nn.json`
  - `reviews_analyzed/adv_jj.json`
  - `reviews_analyzed/adv_jj_pruned.json`
    - only includes ADV+JJ pairs where ADV appears in `intensifiers_20160609_3.json`

## Compare

Compare the Yelp reviews' adjective coverage to JJGraph (all 3 versions).

```sh
$ python compare_reviews.py
```

Input:
  - `reviews_analyzed/jj.json`
  - `graphs/*`

Scripts:
  - `compare_reviews.py`

Output:
  - stats to stdout

