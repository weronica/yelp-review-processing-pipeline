import json
import re
import sys

import networkx as nx

TOTAL_ARGS = 3
FILENAME_ARG = 1


def main():
    # All infiles must be in `yelp_academic_dataset/reviews_parsed/<filename>`:
    parsed_review_dataset = 'yelp_academic_dataset/reviews_parsed/' + sys.argv[FILENAME_ARG]
    # All outfiles will be placed in `yelp_academic_dataset/reviews_processed/<filename>`:
    processed_review_dataset = 'yelp_academic_dataset/reviews_processed/' + sys.argv[FILENAME_ARG]
    # All outfiles (new content only) will be placed in `yelp_academic_dataset/reviews_processed_sm/<filename>`:
    processed_review_dataset_sm = 'yelp_academic_dataset/reviews_processed_sm/' + sys.argv[FILENAME_ARG]
    revs = []

    with open(parsed_review_dataset, 'r') as infile:
        # Every file starts with a blank line.
        next(infile)

        for line in infile:
            rev = json.loads(line)
            # Indicates JVM ran out of memory.
            if len(rev['td']) != len(rev['wt']):
                continue
            revs.append(rev)

    for review in revs:
        nns = set()
        nns_loc = []
        jjs = set()
        jjs_loc = []
        # i = sentence index
        for i, sentence in enumerate(review['wt']):
            # j = word index
            for j, tagged in enumerate(sentence):
                delim = tagged.rfind('/')
                word = tagged[0:delim].lower()
                pos = tagged[delim + 1:]
                if pos == 'NN' or pos == 'NNS':
                    # ROOT = 0, so we add 1 to j
                    nns.add(word)
                    nns_loc.append((word, i, j + 1))
                if pos == 'JJ':
                    # ROOT = 0, so we add 1 to j
                    jjs.add(word)
                    jjs_loc.append((word, i, j + 1))

        # Construct a graph to represent dependency relationships in sentence.
        sentence_graphs = []
        for sentence in review['td']:
            g = nx.DiGraph()
            for rel in sentence:
                delim_lparen = rel.find('(')
                delim_comma = rel.find(',')
                delim_rparen = rel.find(')')
                rel_type = rel[0:delim_lparen]
                rel_src = rel[delim_lparen + 1:delim_comma].lower()
                rel_dest = rel[delim_comma + 2:delim_rparen].lower()
                g.add_edge(rel_src, rel_dest)
                g[rel_src][rel_dest]['type'] = rel_type
            sentence_graphs.append(g)

        # Find JJ+NN and ADV+JJ pairs in sentence.
        jj_nns = []
        jj_nn_loc = []
        adv_jjs = []
        adv_jj_loc = []
        for nn, sentence_indx, word_indx in nns_loc:
            g = sentence_graphs[sentence_indx]
            nn_node = nn + '-' + str(word_indx)
            for dest in g.successors(nn_node):
                src = nn_node
                rel_type = g[src][dest]['type']
                # TODO: Check for negation ('neg')
                # TODO: Handle 'compound'
                if rel_type == 'amod' or rel_type == 'nsubj' or rel_type == 'advmod':
                    # src = nn
                    src_delim = src.rfind('-')
                    nn = src[0:src_delim]
                    nn_loc = int(re.search(r'\d+', src[src_delim+1:]).group())
                    # dest = jj
                    dest_delim = dest.rfind('-')
                    jj = dest[0:dest_delim]
                    jj_loc = int(re.search(r'\d+', dest[dest_delim+1:]).group())
                    # Save info.
                    jj_nns.append([jj, nn])
                    jj_nn_loc.append([jj, jj_loc, nn, nn_loc, rel_type, sentence_indx])
                # Double-counting advmod, but that's fine.
                if rel_type == 'advmod':
                    # src = jj
                    src_delim = src.rfind('-')
                    jj = src[0:src_delim]
                    jj_loc = int(re.search(r'\d+', src[src_delim+1:]).group())
                    # dest = adv
                    dest_delim = dest.rfind('-')
                    adv = dest[0:dest_delim]
                    adv_loc = int(re.search(r'\d+', dest[dest_delim+1:]).group())
                    # Save info.
                    adv_jjs.append([adv, jj])
                    adv_jj_loc.append([adv, adv_loc, jj, jj_loc, rel_type, sentence_indx])

            for src in g.predecessors(nn_node):
                dest = nn_node
                rel_type = g[src][dest]['type']
                if rel_type == 'nsubj':
                    src_delim = src.rfind('-')
                    dest_delim = dest.rfind('-')
                    jj = src[0:src_delim]
                    jj_loc = int(re.search(r'\d+', src[src_delim+1:]).group())
                    nn = dest[0:dest_delim]
                    nn_loc = int(re.search(r'\d+', dest[dest_delim+1:]).group())
                    jj_nns.append([jj, nn])
                    jj_nn_loc.append([jj, jj_loc, nn, nn_loc, rel_type, sentence_indx])

        # Save nouns and adjectives in JSON.
        review['nn'] = list(nns)
        review['nn_loc'] = nns_loc
        review['jj'] = list(jjs)
        review['jj_loc'] = jjs_loc
        review['jj_nn'] = jj_nns
        review['jj_nn_loc'] = jj_nn_loc
        review['adv_jj'] = adv_jjs
        review['adv_jj_loc'] = adv_jj_loc

    # Save text and parser representations to JSON file.
    new_keys = [
        'review_id',
        'nn',
        'nn_loc',
        'jj',
        'jj_loc',
        'jj_nn',
        'jj_nn_loc',
        'adv_jj',
        'adv_jj_loc'
    ]
    for review in revs:
        with open(processed_review_dataset, 'a') as outfile:
            outfile.write('\n')
            json.dump(review, outfile)
        with open(processed_review_dataset_sm, 'a') as outfile_sm:
            review_sm = {k: review[k] for k in new_keys}
            outfile_sm.write('\n')
            json.dump(review_sm, outfile_sm)


if __name__ == '__main__':
    main()
