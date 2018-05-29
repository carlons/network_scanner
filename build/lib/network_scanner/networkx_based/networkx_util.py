import networkx as nx
import os
import operator


def get_pagerank(net, label, outpath):
    """
    get pagerank value
    :param net:
    :param label:
    :param outpath:
    :return:
    """
    if not nx.is_directed(net):
        print('only for directed graph')
        return
    pagerank_value = sorted(nx.pagerank(net).items(), key=operator.itemgetter(1), reverse=True)
    pagerank_file = outpath + label + '-pagerank-top100'
    nodes_id, pagerank_values = zip(*pagerank_value)
    pagerank_ranking = open(pagerank_file, 'w')
    for i in range(100):
        pagerank_ranking.write(str(nodes_id[i]) + '\t' + str(pagerank_values[i]) + '\n')
    pagerank_ranking.close()
    return nodes_id, pagerank_values


if __name__ == '__main__':
    # parameters
    filepath = "/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/NELL/nell-all-id-pair"
    label = "nell-all-id-pair"
    outpath = './output/' + label + '/'

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    net = nx.read_edgelist(filepath, create_using=nx.DiGraph())
    get_pagerank(net, label, outpath)