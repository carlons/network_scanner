import snap
import operator
import os


def get_pagerank(net, label, outpath):
    """
    get pagerank value. For directed graph
    :param net:
    :param label:
    :param outpath:
    :return:
    """
    PRankH = snap.TIntFltH()
    snap.GetPageRank(net, PRankH)
    pagerank_file = open(outpath + label + '-pagerank', 'w')
    pagerank_top_file = open(outpath + label + '-pagerank-top100', 'w')
    pagerank_value = {}
    for item in PRankH:
         pagerank_value[item] = PRankH[item]
    pagerank_value = sorted(pagerank_value.items(), key=operator.itemgetter(1), reverse=True)
    nodes_id, pagerank_values = zip(*pagerank_value)
    for i in range(len(nodes_id)):
        pagerank_file.write(str(nodes_id[i]) + '\t' + str(pagerank_values[i]) + '\n')
    for i in range(100):
        pagerank_top_file.write(str(nodes_id[i]) + '\t' + str(pagerank_values[i]) + '\n')
    pagerank_file.close()
    pagerank_top_file.close()
    return nodes_id, pagerank_values


def get_eigen_vector_centr(net, label, outpath):
    """
    get eigen vector centrality. For undirected graph
    :param net:
    :param label:
    :param outpath:
    :return:
    """
    NIdEigenH = snap.TIntFltH()
    snap.GetEigenVectorCentr(net, NIdEigenH)
    eigen_vector_centr_file = open(outpath + label + '-eigen_vector_centr', 'w')
    eigen_vector_centr_top_file = open(outpath + label + '-eigen_vector_centr-top100', 'w')
    eigen_vector_centr = {}
    for item in NIdEigenH:
        eigen_vector_centr[item] = NIdEigenH[item]
    eigen_vector_centr = sorted(eigen_vector_centr.items(), key=operator.itemgetter(1), reverse=True)
    id, value = zip(*eigen_vector_centr)
    for i in range(len(id)):
        eigen_vector_centr_file.write(str(id[i]) + '\t' + str(value[i]) + '\n')
    for i in range(100):
        eigen_vector_centr_top_file.write(str(id[i]) + '\t' + str(value[i]) + '\n')
    eigen_vector_centr_file.close()
    eigen_vector_centr_top_file.close()
    return id, value


def get_hits(net, label, outpath):
    """
    get hits centrality. For directed graph
    :param net:
    :param label:
    :param outpath:
    :return:
    """
    NIdHubH = snap.TIntFltH()
    NIdAuthH = snap.TIntFltH()
    snap.GetHits(net, NIdHubH, NIdAuthH)
    hub_file = open(outpath + label + '-hub', 'w')
    hub_top_file = open(outpath + label + '-hub-top100', 'w')
    authority_file = open(outpath + label + '-authority', 'w')
    authority_top_file = open(outpath + label + '-authority-top100', 'w')
    # process hub
    hub = {}
    for item in NIdHubH:
        hub[item] = NIdHubH[item]
    hub = sorted(hub.items(), key=operator.itemgetter(1), reverse=True)
    hub_id, hub_value = zip(*hub)
    for i in range(len(hub_id)):
        hub_file.write(str(hub_id[i]) + '\t' + str(hub_value[i]) + '\n')
    for i in range(100):
        hub_top_file.write(str(hub_id[i]) + '\t' + str(hub_value[i]) + '\n')
    # process authority
    authority = {}
    for item in NIdAuthH:
        authority[item] = NIdAuthH[item]
    authority = sorted(authority.items(), key=operator.itemgetter(1), reverse=True)
    authority_id, authority_value = zip(*authority)
    for i in range(len(authority_id)):
        authority_file.write(str(authority_id[i]) + '\t' + str(authority_value[i]) + '\n')
    for i in range(100):
        authority_top_file.write(str(authority_id[i]) + '\t' + str(authority_value[i]) + '\n')
    hub_file.close()
    hub_top_file.close()
    authority_file.close()
    authority_top_file.close()
    return hub, authority


def get_betweenness_centr(net, label, outpath):
    """
    get betweenness centrality.
    :param net:
    :param label:
    :param outpath:
    :return:
    """
    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(net, Nodes, Edges, 1.0)
    node_betweenness_centr_file = open(outpath + label + '-node_btweennesss_centr', 'w')
    node_betweenness_centr_top_file = open(outpath + label + '-node_betweenness_centr-top100', 'w')
    node_betweenness_centr = {}
    for item in Nodes:
        node_betweenness_centr[item] = Nodes[item]
    node_betweenness_centr = sorted(node_betweenness_centr.items(), key=operator.itemgetter(1), reverse=True)
    id, value = zip(*node_betweenness_centr)
    for i in range(len(id)):
        node_betweenness_centr_file.write(str(id[i]) + '\t' + str(value[i]) + '\n')
    for i in range(100):
        node_betweenness_centr_top_file.write(str(id[i]) + '\t' + str(value[i]) + '\n')
    node_betweenness_centr_file.close()
    node_betweenness_centr_top_file.close()
    return id, value


if __name__ == '__main__':
    # parameters
    # filepath = '../input/Test/toy_graph'
    filepath = "/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/YAGO3/facts-id-pair"
    label = "facts-id-pair"
    outpath = './output/' + label + '/'

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    net = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    paras = {'net': net, 'label': label, 'outpath': outpath}
    get_pagerank(**paras)
    get_hits(**paras)
    net = snap.LoadEdgeList(snap.PUNGraph, filepath, 0, 1)
    paras = {'net': net, 'label': label, 'outpath': outpath}
    get_eigen_vector_centr(**paras)