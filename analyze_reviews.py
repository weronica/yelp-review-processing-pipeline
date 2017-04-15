from collections import Counter, OrderedDict
import json
from operator import itemgetter
import os


def main():
    inpath = 'yelp_academic_dataset/reviews_processed_sm/'
    outpath = 'yelp_academic_dataset/reviews_analyzed/'

    with open('intensifiers_20160609_3.json', 'r') as infile:
        intensifiers = json.load(infile)
        intensifiers = [x[0] for x in Counter(intensifiers).most_common(300)]

    nns = {}
    jjs = {}
    jj_nns = {}
    adv_jjs = {}
    adv_jjs_pruned = {}

    for filename in os.listdir(inpath):
        if filename.endswith('.json'):
            with open(inpath + filename, 'r') as infile:
                # Every file starts with a blank line.
                next(infile)

                revs = []
                for line in infile:
                    rev = json.loads(line)
                    revs.append(rev)

                for rev in revs:
                    for nn in rev['nn']:
                        update(nns, nn)
                    for jj in rev['jj']:
                        update(jjs, jj)
                    for jj_nn in rev['jj_nn']:
                        jj = jj_nn[0]
                        nn = jj_nn[1]
                        update(jj_nns, jj + ' ' + nn)
                    for adv_jj in rev['adv_jj']:
                        adv = adv_jj[0]
                        jj = adv_jj[1]
                        update(adv_jjs, adv + ' ' + jj)
                        if adv in intensifiers:
                            update(adv_jjs_pruned, adv + ' ' + jj)

    dict_to_json(jjs, outpath + 'jj.json', sort_values=True)
    dict_to_json(nns, outpath + 'nn.json', sort_values=True)
    dict_to_json(jj_nns, outpath + 'jj_nn.json', sort_values=True)
    dict_to_json(adv_jjs, outpath + 'adv_jj.json', sort_values=True)
    dict_to_json(adv_jjs_pruned, outpath + 'adv_jj_pruned.json', sort_values=True)


def update(d, key):
    if key in d:
        incr(d, key)
    else:
        add(d, key)


def incr(d, key):
    d[key] = d[key] + 1


def add(d, key):
    d[key] = 1


def dict_to_json(data, json_filename, sort_values=False):
    """
    Save a python dict to a file.
    """
    with open(json_filename, 'w') as outfile:
        if not sort_values:
            json.dump(data, outfile, indent=4, sort_keys=True)
        else:
            data = OrderedDict(sorted(data.items(), key=itemgetter(1), reverse=True))
            json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    main()
