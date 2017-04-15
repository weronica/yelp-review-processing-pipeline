import json
import os
import sys

TOTAL_ARGS = 3
FILENAME_ARG = 1
SYS_ARG = 2


def main():
    if len(sys.argv) != TOTAL_ARGS or \
        (sys.argv[SYS_ARG] != '-mac' and sys.argv[SYS_ARG] != '-nlp'):
        print('usage: extract_reviews.py <filename> <-mac/-nlp>')
        exit(1)
    if sys.argv[SYS_ARG] == '-mac':
        system = 'mac'
    elif sys.argv[SYS_ARG] == '-nlp':
        system = 'nlp'
    else:
        exit(1)

    # All infiles must be in `yelp_academic_dataset/reviews_raw/<filename>`:
    review_dataset = 'yelp_academic_dataset/reviews_raw/' + sys.argv[FILENAME_ARG]
    # All outfiles will be placed in `yelp_academic_dataset/reviews_parsed/<filename>`:
    review_text_dataset = 'yelp_academic_dataset/reviews_parsed/' + sys.argv[FILENAME_ARG]
    revs = []

    # Extract review ID, text from JSON file.
    with open(review_dataset, 'r') as infile:
        for line in infile:
            review = json.loads(line)

            id = review['review_id']
            text = review['text'].encode('ascii', 'replace')
            rev = {
                'review_id': id,
                'text': text
            }

            revs.append(rev)

    # Calculate several parser representations for each review's text.
    jars = ['stanford-parser.jar',
            'stanford-parser-3.6.0-sources.jar',
            'stanford-parser-3.6.0-models.jar',
            'stanford-parser-3.6.0-javadoc.jar',
            'slf4j-simple.jar',
            'slf4j-api.jar',
            'ejml-0.23.jar']

    # Set Java class path based on machine.
    class_path = ''
    if system == 'mac':
        class_path = ''.join('/usr/local/Cellar/stanford-parser/3.6.0/libexec/%s:' % x for x in jars)
    elif system == 'nlp':
        class_path = '/nlp/users/whartonv/scalar_adj/code/yelp/stanford-parser/*:'
    tmp_path = 'tmp/' + sys.argv[FILENAME_ARG]

    wt_cmd = 'java -mx150m -cp "%s" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "wordsAndTags" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz %s.txt' % (class_path, tmp_path)
    penn_cmd = 'java -mx150m -cp "%s" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz %s.txt' % (class_path, tmp_path)
    td_cmd = 'java -mx150m -cp "%s" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "typedDependencies" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz %s.txt' % (class_path, tmp_path)
    for rev in revs:
        # Create a temporary file containing the review text, which is
        # necessary for the parser.
        create_tmp(name=tmp_path, contents=rev['text'])

        # Words & tags.
        p = os.popen(wt_cmd, 'r')
        wt_lines = []
        while True:
            line = p.readline().rstrip()
            if not line:
                break
            # Every parsed sentence is followed by an empty line.
            p.readline()
            wt_lines.append(line.split(' '))

        # Penn.
        p = os.popen(penn_cmd, 'r')
        penn_lines = []
        while True:
            penn_line = ''
            line = p.readline().rstrip()
            if not line:
                break
            while True:
                penn_line += line
                line = p.readline().rstrip()
                if not line:
                    penn_lines.append(' '.join(penn_line.split()))
                    break

        # Typed dependencies
        p = os.popen(td_cmd, 'r')
        td_lines = []
        while True:
            td_line = []
            line = p.readline().rstrip()
            if not line:
                break
            while True:
                td_line.append(line)
                line = p.readline().rstrip()
                if not line:
                    td_lines.append(td_line)
                    break

        # Save data in JSON.
        rev['wt'] = wt_lines
        rev['penn'] = penn_lines
        rev['td'] = td_lines

        # Remove temporary file.
        remove_tmp(name=tmp_path)

    # Save text and parser representations to JSON file.
    for rev in revs:
        with open(review_text_dataset, 'a') as outfile:
            outfile.write('\n')
            json.dump(rev, outfile)


def create_tmp(name, contents):
    with open(str(name) + '.txt', 'w') as tmp_file:
        tmp_file.write(contents)


def remove_tmp(name):
    import os
    os.remove(str(name) + '.txt')


if __name__ == '__main__':
    main()
