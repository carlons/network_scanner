import networkit
from networkit import *
import matplotlib.pyplot as plt
import numpy as np
import network_scanner.networkit_based.networkit_util as networkit_util


"""
    plot function
        - (in/out) degree distribution
        - cumulative (in/out) degree distribution
        - in-degree vs out-degree
        - cumulative clustering coefficient
        - assorsativity of degree
        - (@_@)... clustering coefficient VS degree
        - (@_@)... triangle distribution
        - shortest path
        - (@_@)... spectral of adjacency matrix
        - (@_@)... spectral of laplacian matrix
"""


def plot_degree_dist(net, label, outpath):
    """
    plot degree distribution
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: unique degree list
    
    """
    unique_deg, unique_cnt = networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='all')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(unique_deg, unique_cnt, 'b*', label=label)
    # ax.set_title('Degree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('P(x=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-degree-distribution.eps')
    return unique_deg


def plot_indeg_dist(net, label, outpath):
    """
    plot in-degree distribution
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: unique in-degree list
    
    """
    unique_deg, unique_cnt = networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='in')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(unique_deg, unique_cnt, 'g*', label=label)
    # ax.set_title('In-Degree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('P(x=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-indegree-distribution.eps')
    return unique_deg


def plot_outdeg_dist(net, label, outpath):
    """
    plot out-degree distribution
        
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: unique out-degree list
    
    """
    unique_deg, unique_cnt = networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='out')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(unique_deg, unique_cnt, 'r*', label=label)
    # ax.set_title('Out-Degree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('P(x=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-outdegree-distribution.eps')
    return unique_deg


def plot_ccum_degree_dist(net, label, outpath, degree_type='all'):
    """
    plot complementary cumulative degree distribution
        
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: figure
    
    """
    unique_deg, unique_cnt = networkit_util.get_cc_deg_dist(net, degree_type)
    title = {'all': '', 'in': 'In', 'out': 'Out'}
    outfile_name = {'all': 'cc', 'in': 'cc-in', 'out': 'cc-out'}
    marker_color = {'all': 'b', 'in': 'g', 'out': 'r'}
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(unique_deg, unique_cnt, color=marker_color[degree_type], marker='*', label=label)
    # ax.set_title('Complementary Cumulative ' + title[degree_type] + '-Degree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('P(x>=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-' + outfile_name[degree_type] + '-degree-distribution.eps')
    return ax


def plot_out_in_degree_comparision(net, label, outpath):
    """
    plot outdegree-indegree comparision
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: None
    
    """
    zipped_seq = [(net.degreeOut(node), net.degreeIn(node)) for node in net.nodes()]
    out_deg_seq, in_deg_seq = zip(*zipped_seq)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(out_deg_seq, in_deg_seq, 'b.', markersize=1)
    # ax.set_title('Outdegree/Indegree comparision')
    ax.set_xlabel('outdegree')
    ax.set_ylabel('indegree')
    plt.savefig(outpath + label + '-outdegree-indegree-comparision.eps')


def plot_cum_clustering_dist(net, label, outpath):
    """
    cumulative distribution of clustering coefficient of nodes.
    
    ONLY for Undirected graph
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: None
    
    """
    net.removeSelfLoops()
    local_cc = networkit.centrality.LocalClusteringCoefficient(net, turbo=False)
    local_cc.run()
    unique_cc, unique_cc_cnt = np.unique(local_cc.scores(), return_counts=True)
    unique_cc_cumcnt = np.cumsum(unique_cc_cnt)/sum(unique_cc_cnt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.axis([0, 1, 0, 1])
    ax.plot(unique_cc, unique_cc_cumcnt, 'b-')
    # ax.set_title('Cumulative distribution of clustering coefficient of nodes')
    ax.set_xlabel('local clustering coefficient c')
    ax.set_ylabel('p(x <= c)')
    plt.savefig(outpath + label + "-cc-distribution.eps")


def plot_assorsativity(net, label, outpath, degree_type='all'):
    """
    plot degree assorsativity
    
    ONLY support Undirected graph for now.
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: None
    
    """
    deg_seq, nbdeg_seq = networkit_util.get_deg_nbdeg(net, degree_type)
    title = {'all': '', 'in': 'In-', 'out': 'Out-'}
    outfile_name = {'all': 'assorsativity', 'in': 'assorsativity-in', 'out': 'assorsativity-out'}
    marker_color = {'all': 'b', 'in': 'g', 'out': 'r'}
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(deg_seq, nbdeg_seq, marker_color[degree_type]+'.', markersize=1)
    # ax.set_title(title[degree_type] + 'Degreee assortativity')
    ax.set_xlabel(degree_type + '-degree')
    ax.set_ylabel('average neighbour ' + degree_type + '-degree')
    plt.savefig(outpath + label + '-' + outfile_name[degree_type] + '-assortativity-plot.eps')


def plot_connected_component_dist(net, label, outpath):
    """
    plot connected components of undirected graph
        
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: connected component size distribution
    
    """
    cc = networkit_util.get_connected_components(net)
    cc_size, cc_cnt = np.unique(cc, return_counts=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(cc_size, cc_cnt, 'r*', label=label)
    # ax.set_title('Connected components distribution')
    ax.set_xlabel('size')
    ax.set_ylabel('count')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-connected-component-distribution.eps')
    return cc


def plot_wcc_dist(net, label, outpath):
    """
    plot weakly connected components of directed graph
        
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :return: weakly connected component size distribution
    
    """
    wcc = networkit_util.get_wcc(net)
    wcc_size, wcc_cnt = np.unique(wcc, return_counts=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(wcc_size, wcc_cnt, 'b*', label=label)
    # ax.set_title('Weakly connected components distribution')
    ax.set_xlabel('size')
    ax.set_ylabel('count')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-wcc-distribution.eps')
    return wcc


def plot_scc_dist(net, label, outpath):
    """
    plot strongly connected components of directed graph

    :param net: networkit graph object

    :param label: network label

    :param outpath: figure output directory

    :return: strongly connected component size distribution

    """
    scc = networkit_util.get_scc(net)
    scc_size, scc_cnt = np.unique(scc, return_counts=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(scc_size, scc_cnt, 'g*', label=label)
    # ax.set_title('Strongly connected components distribution')
    ax.set_xlabel('size')
    ax.set_ylabel('count')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-scc-distribution.eps')
    return scc


def plot_betweeness(net, label, outpath):
    """
    plot cumulative betweenss centrality
    
    :param net: networkit graph object

    :param label: network label

    :param outpath: figure output directory
    
    :return: None
    
    """
    _, betweeness_values = networkit_util.get_betweeness(net, label, outpath)
    unique_value, unique_cnt = np.unique(betweeness_values, return_counts=True)
    unique_cumcnt = np.cumsum(unique_cnt) / sum(unique_cnt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(unique_value, unique_cumcnt, 'b.')
    # ax.set_title('Cumulative distribution of betweeness centrality of nodes')
    ax.set_xlabel('betweeness centrality b')
    ax.set_ylabel('p(x <= b)')
    plt.savefig(outpath + label + "-betweeness-distribution.eps")


def plot_eigenvector_centrality(net, label, outpath):
    """
    plot cumulative eigenvector centrality

    :param net: networkit graph object

    :param label: network label

    :param outpath: figure output directory

    :return: None
    
    """
    _, eigenvector_centrality_values = networkit_util.get_eigenvector_centrality(net, label, outpath)
    unique_value, unique_cnt = np.unique(eigenvector_centrality_values, return_counts=True)
    unique_cumcnt = np.cumsum(unique_cnt) / sum(unique_cnt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(unique_value, unique_cumcnt, 'g.')
    # ax.set_title('Cumulative distribution of eigenvector centrality of nodes')
    ax.set_xlabel('eigenvector centrality e')
    ax.set_ylabel('p(x <= e)')
    plt.savefig(outpath + label + "-eigenvector-distribution.eps")


def plot_pagerank(net, label, outpath):
    """
    plot cumulative pagerank centrality

    :param net: networkit graph object

    :param label: network label

    :param outpath: figure output directory

    :return: None
    """
    _, pagerank_values = networkit_util.get_pagerank(net, label, outpath)
    unique_value, unique_cnt = np.unique(pagerank_values, return_counts=True)
    unique_cumcnt = np.cumsum(unique_cnt) / sum(unique_cnt)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(unique_value, unique_cumcnt, 'r.')
    # ax.set_title('Cumulative distribution of pagerank of nodes')
    ax.set_xlabel('pagerank value v')
    ax.set_ylabel('p(x <= v)')
    plt.savefig(outpath + label + "-pagerank-distribution.eps")


def plot_hop_dist(net, label, outpath):
    """
    plot hop distribution.only support connected graph
    
    :param net: networkit graph object

    :param label: network label

    :param outpath: figure output directory
    
    :return: None
   
    """
    dist, proportion = networkit_util.get_hop_distr(net, label, outpath)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dist, proportion, 'g*', label=label)
    ax.set_xlabel('distance d')
    ax.set_ylabel('p(x<=d)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-hop.eps')


if __name__ == '__main__':
    # filepath = "../input/cit-HepTh"
    # label = "cit-Hepth"
    # outpath = './output/' + label + '/'
    # net = graphio.readGraph(filepath, Format.EdgeList, separator=' ', firstNode=0, continuous=False, directed=True)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # plot_degree_dist(**paras)
    # plot_indeg_dist(**paras)
    # plot_outdeg_dist(**paras)

    # degree_type = 'out'
    # paras = {'net': net, 'label': label, 'outpath': outpath, 'degree_type': degree_type}
    # plot_ccum_degree_dist(**paras)

    # plot_out_in_degree_comparision(**paras)
    # net = graphio.readGraph(filepath, Format.EdgeList, separator=' ', firstNode=0, continuous=False, directed=False)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # plot_cum_clustering_dist(**paras)

    # degree_type = 'all'
    # paras = {'net': net.toUndirected(), 'label': label, 'outpath': outpath, 'degree_type': degree_type}
    # plot_assorsativity(**paras)

    # plot_wcc_dist(**paras)
    # plot_scc_dist(**paras)

    # plot_betweeness(**paras)
    # plot_eigenvector_centrality(**paras)
    # plot_pagerank(**paras)

    filepath = "/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/NELL/nell-all-id-pair"
    net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    subgraph = networkit_util.get_lcc_subgraph(net)
    label = 'test-hopplot'
    outpath = './output/'
    plot_hop_dist(subgraph, label, outpath)