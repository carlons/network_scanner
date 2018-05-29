#coding=utf-8
import os
import collections
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

"""
    plot function
        - in-degree distribution
        - out-degree distribution
        - degree distribution
        - in-degree vs out-degree
        - clustering coefficient distribution
        - cumulative clustering coefficient
        - triangle distribution
        - assorsativity of degree
        - assorsativity of in-degree
        - assorsativity of out-degree
        - shortest path
        - spectral of adjacency matrix
        - spectral of laplacian matrix
        - average neighbour degree VS degree
        - average clustering coefficient VS degree
"""


def _ccd_indeg(graph, filename):
    """ get complementary cumulative in-degree distribution """
    if not graph:
        graph = nx.read_edgelist(filename, create_using=nx.DiGraph())
    # Old solution.
    # size = nx.number_of_nodes(graph)
    # in_deg_seq = np.array(dict(graph.in_degree()).values())
    # in_deg_unique = np.unique(in_deg_seq)
    # in_deg_hist = np.array([ele for ele in np.bincount(in_deg_seq) if ele != 0])
    # in_deg_cumsum = np.flip(np.cumsum(np.flip(in_deg_hist, 0)) / (size + 0.0), 0)

    # New solution
    in_deg_seq = sorted([d for n, d in graph.in_degree()], reverse=True)
    in_deg_cnt = collections.Counter(in_deg_seq)
    #in_deg_unique, in_deg_c =
    #in_ccdf = [in_deg_unique, in_deg_cumsum]
    #return in_ccdf


def plot_in_degree_dist(graph, filename, label, outpath):
    """ plot cc in-degree distribution """
    in_ccdf = _ccd_indeg(graph, filename)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(in_ccdf[0], in_ccdf[1], 'k*', label=label)
    ax.set_title('Indegree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('p(x>=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-indegree distribution.svg')


def _ccd_outdeg(graph, filename):
    """ get complementary cumulative out-degree distribution """
    graph = nx.read_edgelist(filename, create_using=nx.DiGraph())
    size = nx.number_of_nodes(graph)
    out_deg_seq = np.array(dict(graph.out_degree()).values())
    out_deg_unique = np.unique(out_deg_seq)
    out_deg_hist = np.array([ele for ele in np.bincount(out_deg_seq) if ele != 0])
    out_deg_cumsum = np.flip(np.cumsum(np.flip(out_deg_hist, 0)) / (size + 0.0), 0)
    in_ccdf = [out_deg_unique, out_deg_cumsum]
    return in_ccdf


def plot_out_degree_dist(graph, filename, label, outpath):
    """ plot cc out-degree distribution """
    out_ccdf = _ccd_outdeg(graph, filename)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(out_ccdf[0], out_ccdf[1], 'k*', label=label)
    ax.set_title('Outdegree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('p(x>=k)')
    ax.legend(loc='best')
    plt.savefig(outpath + label + '-outdegree distribution.svg')


def _ccf(graph, filename=None):
    """ get complementary cumulative frequency """
    if not graph:
        graph = nx.read_edgelist(filename)
    degree_hist = nx.degree_histogram(graph)
    degree_hist_array = np.array(degree_hist)
    non_zeros = 0
    for elem in degree_hist:
        if elem != 0:
            non_zeros = non_zeros + 1
    cc_freq = np.array(np.zeros((non_zeros, 2)), np.int32)
    rows = 0
    for i in range(1, len(degree_hist_array)):
        if degree_hist_array[i] == 0:
            continue
        else:
            cc_freq[rows, :] = [i, sum(degree_hist_array[i:])]
            rows = rows + 1
    return cc_freq


def plot_degree_dist(graph, filename, label, outpath):
    """ plot ccf degree distribution """
    cc_freq = _ccf(graph, filename)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(cc_freq[:, 0], cc_freq[:, 1], 'k*', label=label)
    ax.set_title('Degree distribution')
    ax.set_xlabel('k')
    ax.set_ylabel('complementary cumulative frequency')
    ax.legend(loc='best')
    plt.savefig(outpath + 'degree distribution.svg')
    return ax


# def degree_dist(filename, model_one_filename, model_two_filename):
#     """ plot ccf degree distribution """
#     cc_freq = ccf(filename)
#     cc_freq_one = ccf(model_one_filename)
#     cc_freq_two = ccf(model_two_filename)
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.loglog(cc_freq[:, 0], cc_freq[:, 1], 'k*', label='email')
#     ax.loglog(cc_freq_one[:, 0], cc_freq_one[:, 1], 'bo', label='NRM')
#     ax.loglog(cc_freq_two[:, 0], cc_freq_two[:, 1], 'g1', label='FFM')
#     ax.set_title('Degree distribution')
#     ax.set_xlabel('k')
#     ax.set_ylabel('complementary cumulative frequency')
#     ax.legend(loc='best')
#     plt.savefig('degree distribution.svg')


def plot_out_in_degree_comparision(graph, filename, label, outpath):
    """ plot outdegree-indegree comparision """
    if not graph:
        graph = nx.read_edgelist(filename, create_using=nx.DiGraph())
    in_deg_seq = dict(graph.in_degree()).values()
    out_deg_seq = dict(graph.out_degree()).values()
    # print in_deg_seq
    # print out_deg_seq
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(out_deg_seq, in_deg_seq, 'b.', markersize=1)
    ax.set_title('Outdegree/Indegree comparision')
    ax.set_xlabel('outdegree')
    ax.set_ylabel('indegree')
    plt.savefig(outpath + label + '-outdegree-indegree comparision.svg')


def _clustering_cf(graph, filename):
    """ get clustering coefficient of each node """
    if not graph:
        graph = nx.read_edgelist(filename)
    clustering_cf = nx.clustering(graph)
    clustering_cf_list = []
    for key in clustering_cf.keys():
        clustering_cf_list.append(clustering_cf[key])
    sorted_list = sorted(clustering_cf_list, reverse=True)
    return sorted_list


def plot_clustering_dist(graph, filename, label, outpath):
    """ distribution of clustering coefficient of nodes """
    sorted_list = _clustering_cf(graph, filename)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(range(1, len(sorted_list) + 1), sorted_list, 'k*', label=label)
    ax.set_title('Distribution of clustering coefficient of nodes')
    ax.set_xlabel('rank')
    ax.set_ylabel('CC')
    ax.legend(loc='best')
    plt.savefig(outpath + "clustering coefficient distribution.svg")
    return ax


# def clustering_dist(filename, model_one_filename, model_two_filename):
#     """ distribution of clustering coefficient of nodes """
#     sorted_list = clustering_cf(filename)
#     sorted_list_model_one = clustering_cf(model_one_filename)
#     sorted_list_model_two = clustering_cf(model_two_filename)
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.loglog(range(1, len(sorted_list) + 1), sorted_list, 'k*', label='email')
#     ax.loglog(range(1, len(sorted_list_model_one) + 1), sorted_list_model_one, 'bo', label='NRM')
#     ax.loglog(range(1, len(sorted_list) + 1), sorted_list_model_two, 'g1', label='FFM')
#     ax.set_title('Distribution of clustering coefficient of nodes')
#     ax.set_xlabel('rank')
#     ax.set_ylabel('CC')
#     ax.legend(loc='best')
#     plt.savefig("clustering coefficient distribution.svg")


def plot_cum_clustering_dist(graph, filename, label, outpath):
    """ cumulative distribution of clustering coefficient of nodes """
    if not graph:
        graph = nx.read_edgelist(filename)
    size = nx.number_of_nodes(graph)
    local_cc = nx.clustering(graph)
    local_cc_seq = np.array([local_cc[key] for key in local_cc])
    local_cc_unique = np.unique(local_cc_seq, return_counts=True)
    local_cc_cumsum = local_cc_unique[1].cumsum(0)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(local_cc_unique[0], local_cc_cumsum/(size + 0.0), 'b-')
    ax.set_title('Distribution of clustering coefficient of nodes')
    ax.set_xlabel('local clustering coefficient c')
    ax.set_ylabel('p(x <= c)')
    plt.savefig(outpath + label + "-cc-distribution.svg")


def _triangles(graph, filename):
    """ get triangles of each node """
    if not graph:
        graph = nx.read_edgelist(filename)
    triangles_count = nx.triangles(graph)
    triangles_count_list = []
    for key in triangles_count.keys():
        triangles_count_list.append(triangles_count[key])
    sorted_list = sorted(triangles_count_list, reverse=True)
    return sorted_list


def plot_triangles_dist(graph, filename, label, outpath):
    """ distribution of triangles of nodes """
    sorted_list = _triangles(graph, filename)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(range(1, len(sorted_list) + 1), sorted_list, 'k*', label=label)
    ax.set_title('Distribution of triangles of nodes')
    ax.set_xlabel('rank')
    ax.set_ylabel("Triangles' count")
    plt.savefig(outpath + "triangles distribution.svg")
    return ax


def plot_assorsativity(graph, filename, label, outpath):
    """ plot degree assorsativity """
    if not graph:
        graph = nx.read_edgelist(filename)
    deg_seq = nx.degree(graph)
    avg_nb_deg = nx.average_neighbor_degree(graph)
    deg_avg_nb_deg = np.array([(deg_seq[key], avg_nb_deg[key]) for key in avg_nb_deg])
    # print deg_avg_nb_deg[:,1]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(deg_avg_nb_deg[:, 0], deg_avg_nb_deg[:, 1], 'b.', markersize=1)
    ax.set_title('Degreee assortativity')
    ax.set_xlabel('degree')
    ax.set_ylabel('average neighbour degree')
    plt.savefig(outpath + label + '-assortativity-plot.svg')


def plot_assorsativity_outdegree(graph, filename, label, outpath):
    """ plot outdegree-outdegree assorsativity """
    if not graph:
        graph = nx.read_edgelist(filename, create_using=nx.DiGraph())
    out_deg_seq = graph.out_degree()
    avg_nb_outdeg = nx.average_neighbor_degree(graph, source='out', target='out')
    outdeg_avg_nb_outdeg = np.array([(out_deg_seq[key], avg_nb_outdeg[key]) for key in avg_nb_outdeg])
    # print deg_avg_nb_deg[:,1]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(outdeg_avg_nb_outdeg[:, 0], outdeg_avg_nb_outdeg[:, 1], 'r.', markersize=1)
    ax.set_title('Outdegreee assortativity')
    ax.set_xlabel('outdegree')
    ax.set_ylabel('average neighbour outdegree')
    plt.savefig(outpath + label + '-assortativity-outdegree-plot.svg')


def plot_assorsativity_indegree(graph, filename, label, outpath):
    """ plot indegree-indegree assorsativity """
    if not graph:
        graph = nx.read_edgelist(filename, create_using=nx.DiGraph())
    in_deg_seq = graph.in_degree()
    avg_nb_indeg = nx.average_neighbor_degree(graph, source='in', target='in')
    indeg_avg_nb_indeg = np.array([(in_deg_seq[key], avg_nb_indeg[key]) for key in avg_nb_indeg])
    # print deg_avg_nb_deg[:,1]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(indeg_avg_nb_indeg[:, 0], indeg_avg_nb_indeg[:, 1], 'g.', markersize=1)
    ax.set_title('indegreee assortativity')
    ax.set_xlabel('indegree')
    ax.set_ylabel('average neighbour indegree')
    plt.savefig(outpath + label + '-assortativity-indegree-plot.svg')


def plot_shortest_path_dist(graph, filename, label, outpath):
    """ plot shortest path distribution """
    if not graph:
        graph = nx.read_edgelist(filename)
    subgraph = graph
    if not nx.is_connected(graph):
        lcc_subgraph = max(nx.connected_component_subgraphs(graph), key=len)
        subgraph = lcc_subgraph
    size = nx.number_of_nodes(subgraph)
    p = nx.all_pairs_shortest_path_length(subgraph)
    all_shortest_paths = np.array([i[1].values() for i in p])
    all_shortest_paths_seq = all_shortest_paths.reshape((16,))
    path_unique = np.unique(all_shortest_paths_seq, return_counts=True)
    path_cumsum = path_unique[1].cumsum(0)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(path_unique[0], path_cumsum / (size * size + 0.0), 'b-')
    ax.set_title('shortest path length distribution')
    ax.set_xlabel('shortest path length d')
    ax.set_ylabel('p(x <= d)')
    plt.savefig(outpath + label + '-shortest-path.svg')


def plot_spectral_adj(graph, filename, label, outpath):
    """ plot spectral distribution of adjacency matrix"""
    if not graph:
        graph = nx.read_edgelist(filename)
    spectrals = nx.adjacency_spectrum(graph)
    spectrals_unique = np.unique(spectrals, return_counts=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(spectrals_unique[0], spectrals_unique[1])
    ax.set_title('spectral distribution of adjacency matrix')
    ax.set_xlabel('eigenvalue')
    ax.set_ylabel('frequency')
    plt.savefig(outpath + label + '-spectral-adj.svg')


def plot_spectral_laplacian(graph, filename, label, outpath):
    """ plot spectral distribution of laplacian matrix"""
    if not graph:
        graph = nx.read_edgelist(filename)
    spectrals = nx.laplacian_spectrum(graph)
    spectrals_unique = np.unique(spectrals, return_counts=True)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(spectrals_unique[0], spectrals_unique[1])
    ax.set_title('spectral distribution of laplacian matrix')
    ax.set_xlabel('eigenvalue')
    ax.set_ylabel('frequency')
    plt.savefig(outpath + label + '-spectral-laplacian.svg')

# def triangles_dist(filename, model_one_filename, model_two_filename):
#     """ distribution of triangles of nodes """
#     sorted_list = triangles(filename)
#     sorted_list_model_one = triangles(model_one_filename)
#     sorted_list_model_two = triangles(model_two_filename)
#     fig = plt.figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.loglog(range(1, len(sorted_list) + 1), sorted_list, 'k*', label='email')
#     ax.loglog(range(1, len(sorted_list_model_one) + 1), sorted_list_model_one, 'bo', label='NRM')
#     ax.loglog(range(1, len(sorted_list) + 1), sorted_list_model_two, 'g1', label='FFM')
#     ax.set_title('Distribution of triangles of nodes')
#     ax.set_xlabel('rank')
#     ax.set_ylabel("Triangles' count")
#     ax.legend(loc='best')
#     plt.savefig("triangles distribution.svg")


def _get_total_neighb_deg(graph, node):
    """ get the sum of neighbour degrees of certain node"""
    neighbour_nodes = nx.all_neighbors(graph, node)
    result = 0
    for ele in neighbour_nodes:
        result = result + nx.degree(graph, ele)
    return result


def _get_neighb_deg_deg(graph):
    """ get average neighbour degree VS degree """
    degree_neighbour_degree = dict()
    degree_count = dict()
    # First calculate the sum of neighbour degrees and frequency of each degree
    for node in nx.nodes(graph):
        # print(nx.degree(graph, node))
        total_neighb_deg = _get_total_neighb_deg(graph, node)
        deg = nx.degree(graph, node)
        if deg in degree_neighbour_degree:
            degree_neighbour_degree[deg] = degree_neighbour_degree[deg] + total_neighb_deg
            degree_count[deg] = degree_count[deg] + 1
        else:
            degree_neighbour_degree[deg] = total_neighb_deg
            degree_count[deg] = 1
    # Then calculate average neighbour degree
    for key in degree_neighbour_degree.keys():
        degree_neighbour_degree[key] = degree_neighbour_degree[key] / (key * degree_count[key])
        # print(key, degree_neighbour_degree[key])
    # Sort dict by keys and return tuple
    result = sorted(degree_neighbour_degree.items(), key=lambda item:item[0])
    x = []
    y = []
    for ele in result:
        x.append(ele[0])
        y.append(ele[1])
    result = (x, y)
    return result


def plot_neighb_degree_degree(graph, filename, label, outpath):
    """ plot average neighbour degree vs degree """
    # how to calculate?
    if not graph:
        graph = nx.read_edgelist(filename)
    result = _get_neighb_deg_deg(graph)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(result[0], result[1], 'b-')
    ax.set_title('average neighbour degree VS degree')
    ax.set_xlabel('degree')
    ax.set_ylabel('average neighbour degree')
    # ax.set_ylim(0, 40)
    plt.savefig(outpath + label + '-neighb_deg_deg.svg')


def _get_cls_coeff_deg(graph):
    """ get clustering coefficient VS degree"""
    clustering_degree = dict()
    deg_cnt = dict()
    # First calculate clustering coefficient of each node and degree frequency
    for node in nx.nodes(graph):
        deg = nx.degree(graph, node)
        cls_coeff = nx.clustering(graph, node)
        if deg in clustering_degree:
            clustering_degree[deg] = clustering_degree[deg] + cls_coeff
            deg_cnt[deg] = deg_cnt[deg] + 1
        else:
            clustering_degree[deg] = cls_coeff
            deg_cnt[deg] = 1
    # Then calculate average clustering coefficient for certain degree
    for key in clustering_degree.keys():
        clustering_degree[key] = clustering_degree[key] / deg_cnt[key]
    # Sort dict by keys
    result = sorted(clustering_degree.items(), key=lambda item: item[0])
    x = []
    y = []
    for ele in result:
        x.append(ele[0])
        y.append(ele[1])
    result = (x, y)
    return result


def plot_cls_coeff_deg(graph, filename, label, outpath):
    """ plot average clustering coefficient VS degree """
    if not graph:
        graph = nx.read_edgelist(filename, create_using=nx.Graph())
    result = _get_cls_coeff_deg(graph)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(result[0], result[1], 'b-')
    ax.set_title('average clustering coefficient VS degree')
    ax.set_xlabel('degree')
    ax.set_ylabel('average clustering coefficient')
    plt.savefig(outpath + label + '-cls_coeff_deg.svg')


if __name__ == '__main__':
    # prepare data
    data = "../input/en-yagoFacts-d-r-id-pair.txt"
    label = "en-yagoFacts-d-r-id-pair"
    outpath = "output/yago/"
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # read data
    graph = nx.read_edgelist(data)
    print(nx.info(graph))
    paras = {"graph": graph, "filename": data, "label": label, "outpath": outpath}
    # plot_in_degree_dist(**paras) BUG
    # plot_assorsativity_indegree(**paras) OK
    # plot_assorsativity_outdegree(**paras) OK
    # plot_out_in_degree_comparision(**paras) OK
    # plot_assorsativity(**paras) OK
    # plot_cls_coeff_deg(**paras) Time
    # plot_neighb_degree_degree(**paras) Time
    plot_spectral_adj(**paras)
    plot_spectral_laplacian(**paras)
    plot_triangles_dist(**paras)
    plot_clustering_dist(**paras)
    plot_shortest_path_dist(**paras)
    print('done')