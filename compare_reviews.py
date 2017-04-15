import json
import operator

from networkx.readwrite import json_graph


def main():
    inpath = 'yelp_academic_dataset/reviews_analyzed/'
    graphs = [
        'graphs/graph_20161030.json',
        'graphs/graph_20161106_and.json',
        'graphs/graph_20161106_or.json'
    ]

    with open(inpath + 'jj.json', 'r') as infile:
        jjs = json.load(infile)

    graph_all = from_json(graphs[0])
    graph_and = from_json(graphs[1])
    graph_or = from_json(graphs[2])

    # All adjectives.
    print 'All adjectives:'

    num_all = num_in_graph(jjs.keys(), graph_all)
    num_and = num_in_graph(jjs.keys(), graph_and)
    num_or = num_in_graph(jjs.keys(), graph_or)

    print '\tJJGraph: \t%d / %d (%f)' % stats(num_all, graph_all)
    print '\tJJGraph_AND: \t%d / %d (%f)' % stats(num_and, graph_and)
    print '\tJJGraph_OR: \t%d / %d (%f)' % stats(num_or, graph_or)

    # Top 1000 adjectives.
    print 'Top 1000 most frequent adjectives:'

    sorted_jjs = sorted(jjs.items(), key=operator.itemgetter(1))
    sorted_jjs.reverse()
    sorted_jjs = [i[0] for i in sorted_jjs[0:1000]]

    num_all = num_in_graph(sorted_jjs, graph_all)
    num_and = num_in_graph(sorted_jjs, graph_and)
    num_or = num_in_graph(sorted_jjs, graph_or)

    print '\tJJGraph: \t%d / %d (%f)' % stats(num_all, graph_all)
    print '\tJJGraph_AND: \t%d / %d (%f)' % stats(num_and, graph_and)
    print '\tJJGraph_OR: \t%d / %d (%f)' % stats(num_or, graph_or)


def from_json(filename):
    with open(filename, 'r') as infile:
        networkx_graph = json_graph.node_link_graph(json.load(infile))
        return networkx_graph


def num_in_graph(jjs, graph):
    num = 0
    for jj in jjs:
        if jj in graph:
            num = num + 1
    return num


def stats(jj_overlap_num, graph):
    return (jj_overlap_num, graph.number_of_nodes(), (1. * jj_overlap_num / graph.number_of_nodes()))


if __name__ == '__main__':
    main()
