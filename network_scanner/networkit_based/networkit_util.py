import networkit
from networkit import *
import numpy as np
import scipy.sparse.csgraph
import scipy.sparse.linalg
import scipy.stats
import random


def readnetwork(filepath, directed):
    """
    read network from edgelist file

    :param filepath: edgelist file

    :param directed: boolean, treat the network as directed or not

    :return:

    """
    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=directed)
    net = net_reader.read(filepath)
    return net


def get_deg_dist(net, degree_type='all'):
    """
    get (in/out)degree distribution

    :param net: networkit graph

    :param degree_type: 'all' 'in' 'out'

    :return: https://docs.scipy.org/doc/numpy/reference/generated/numpy.unique.html#numpy.unique

    """
    if degree_type not in ['all', 'in', 'out']:
        print("ERROR degree type.")
        return
    if degree_type == 'all':
        ret = [net.degree(node) for node in net.nodes()]
        return np.unique(ret, return_counts=True)
    if degree_type == 'in':
        ret = [net.degreeIn(node) for node in net.nodes()]
        return np.unique(ret, return_counts=True)
    if degree_type == 'out':
        ret = [net.degreeOut(node) for node in net.nodes()]
        return np.unique(ret, return_counts=True)


def get_and_write_deg_dist(net, label, outpath, degree_type='all'):
    """
    get (in/out)degree distribution

    :param net: networkit graph

    :param label

    :param outpath

    :param degree_type: 'all' 'in' 'out'

    :return: https://docs.scipy.org/doc/numpy/reference/generated/numpy.unique.html#numpy.unique

    """
    if degree_type not in ['all', 'in', 'out']:
        print("ERROR degree type.")
        return
    if degree_type == 'all':
        ret = []
        degree_file = open(outpath + label + '-falseid-degree', 'w')
        for node in net.nodes():
            deg = net.degree(node)
            degree_file.write(str(node) + '\t' + str(deg) + '\n')
            ret.append(deg)
        degree_file.close()
        return np.unique(ret, return_counts=True)
    if degree_type == 'in':
        ret = []
        indegree_file = open(outpath + label + '-falseid-indegree', 'w')
        for node in net.nodes():
            indeg = net.degreeIn(node)
            indegree_file.write(str(node) + '\t' + str(indeg) + '\n')
            ret.append(indeg)
        # ret = [net.degreeIn(node) for node in net.nodes()]
        indegree_file.close()
        return np.unique(ret, return_counts=True)
    if degree_type == 'out':
        ret = []
        outdegree_file = open(outpath + label + '-falseid-outdegree', 'w')
        for node in net.nodes():
            outdeg = net.degreeOut(node)
            outdegree_file.write(str(node) + '\t' + str(outdeg) + '\n')
            ret.append(outdeg)
        # ret = [net.degreeOut(node) for node in net.nodes()]
        outdegree_file.close()
        return np.unique(ret, return_counts=True)


def get_cc_deg_dist(net, degree_type='all'):
    """
    get complementary cumulative degree distribution
    
    :param net: networkit graph object
    
    :param degree_type: 'all' 'in' 'out'
    
    :return: unique value and count
   
   """
    uniqe_ele, unique_cnt = get_deg_dist(net, degree_type)
    tmp_sum = sum(unique_cnt)
    unique_cc_cnt = [sum(unique_cnt[i:])/tmp_sum for i in range(len(unique_cnt))]
    # another solution
    # ant = tmp_sum - np.cumsum(unique_cnt) + unique_cnt
    # ant = ant/tmp_sum
    return uniqe_ele, unique_cc_cnt


def get_deg_nbdeg(net, degree_type='all'):
    """
    get (in/out)degree vs neighbor (in/out)degree
    
    :param net: networkit graph object
    
    :param degree_type: 'all' 'in' 'out'
    
    :return: degree and average neighbour degree
    
    """
    deg_seq = []
    nbdeg_seq = []
    if degree_type == 'all':
        for node in net.nodes():
            deg_seq.append(net.degree(node))
            avg_deg = 0
            node_neighbors = net.neighbors(node)
            if len(node_neighbors) != 0:
                for ele in node_neighbors:
                    # print(net.degree(ele))
                    avg_deg = avg_deg + net.degree(ele)
                # print(avg_deg, len(node_neighbors))
                avg_deg = avg_deg / len(node_neighbors)
            nbdeg_seq.append(avg_deg)
        return deg_seq, nbdeg_seq


def get_reciprocity(net):
    """
    get reciprocity
    
    :param net: networkit graph object
    
    :return: reciprocity value
    
    """
    num_edges = net.numberOfEdges()
    colinks = 0
    for ele in net.edges():
        if net.hasEdge(ele[1], ele[0]):
            colinks += 1
    return colinks / num_edges


def get_spectral_norm(net):
    """
    get spectral norm. time consuming.
    
    :param net: networkit graph object
    
    :return: eigenvalue and eigenvector of adjacent matrix
    
    """
    sparse_adj_matrix = networkit.algebraic.adjacencyMatrix(net, matrixType='sparse')
    paras = {'k': net.numberOfNodes()-2, 'which': 'LM', 'return_eigenvectors': False}
    eig_eigv = scipy.sparse.linalg.eigs(sparse_adj_matrix, **paras)
    return eig_eigv


def get_algebraic_connectivity(net):
    """
    get algebraic connectivity. time consuming. 
    
    :param net: networkit graph object 
    
    :return: eigenvalue and eigenvector of laplacian matrix
    
    """
    sparse_adj_matrix = networkit.algebraic.adjacencyMatrix(net, matrixType='sparse')
    laplacien_matrix = scipy.sparse.csgraph.laplacian(sparse_adj_matrix)
    paras = {'k': 3, 'which': 'SR'}
    eig_eigv = scipy.sparse.linalg.eigs(laplacien_matrix, **paras)
    return eig_eigv


def _node_degree_xy(net, x='out', y='in'):
    for u in net.nodes():
        degu = net.degreeOut(u)
        neighbors = (nbr for nbr in net.neighbors(u))
        for v in neighbors:
            degv = net.degreeIn(v)
            yield degu, degv
    # for source, target in net.edges():
    #     deg_source = net.degreeIn(source)
    #     deg_target = net.degreeOut(target)
    #     yield deg_source, deg_target


def _node_degree_neighbourdegree(net):
    for u in net.nodes():
        deg_u = net.degree(u)
        neighbors_u = net.neighbors(u)
        neighbors_num = len(neighbors_u)
        if not neighbors_num:
            continue
        average_degree = 0
        for nb in neighbors_u:
            average_degree += net.degree(nb)
        average_degree = average_degree / neighbors_num
        yield deg_u, average_degree


def get_assorsativity(net):
    """
    get assorsativity
    
    :param net: networkit graph object
    
    :return: assorsativity value
    
    """
    xy = _node_degree_xy(net)
    x, y = zip(*xy)
    return scipy.stats.pearsonr(x, y)[0]


def get_connected_components(net):
    """
    get sizes of connected components
    
    :param net: networkit graph object
    
    :return: connected component distribution
    
    """
    cc = components.ConnectedComponents(net)
    cc.run()
    num_of_cc = cc.numberOfComponents()
    sizes_of_cc = cc.getComponentSizes()
    cc = [sizes_of_cc[k] for k in sizes_of_cc]
    return cc


def get_wcc(net):
    """
    get sizes of weakly connected components
    
    :param net: networkit graph object
    
    :return: weakly connected component distribution
    
    """
    wcc = components.WeaklyConnectedComponents(net)
    wcc.run()
    num_of_wcc = wcc.numberOfComponents()
    sizes_of_wcc = wcc.getComponentSizes()
    wcc = [sizes_of_wcc[k] for k in sizes_of_wcc]
    return wcc


def get_scc(net):
    """
    get sizes of strongly connected components
    
    :param net: networkit graph object
    
    :return: strongly connected component distribution
    
    """
    scc = components.StronglyConnectedComponents(net)
    scc.run()
    num_of_scc = scc.numberOfComponents()
    scc_partitions = scc.getPartition()
    # reference https://networkit.iti.kit.edu/api/networkit.html?highlight=partition#networkit.Partition
    scc = scc_partitions.subsetSizes()
    return scc


def get_betweeness(net, label, outpath):
    """
    get betweeness centrality
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: node id and betweeness centrality value
    
    """
    betweeness = centrality.ApproxBetweenness(net, epsilon=0.01, delta=0.1, universalConstant=1.0)
    betweeness.run()
    betweeness_file = outpath + label + '-betweeness-falseid-value'
    betweeness_ranking = open(betweeness_file, 'w')
    nodes_id, betweeness_values = zip(*betweeness.ranking())
    for i in range(len(nodes_id)):
        betweeness_ranking.write(str(nodes_id[i]) + '\t' + str(betweeness_values[i]) + '\n')
    betweeness_ranking.close()
    return nodes_id, betweeness_values


def get_eigenvector_centrality(net, label, outpath):
    """
    get eigenvector centrality
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: node id and eigenvector centrality value
    
    """
    eigenvector_centrality = centrality.EigenvectorCentrality(net,  tol=1e-9)
    eigenvector_centrality.run()
    eigenvector_file = outpath + label + '-eigenvector-centrality-falseid-value'
    nodes_id, eigenvector_centrality_values = zip(*eigenvector_centrality.ranking())
    eigenvector_ranking = open(eigenvector_file, 'w')
    for i in range(len(nodes_id)):
        eigenvector_ranking.write(str(nodes_id[i]) + '\t' + str(eigenvector_centrality_values[i]) + '\n')
    eigenvector_ranking.close()
    return nodes_id, eigenvector_centrality_values


def get_pagerank(net, label, outpath):
    """
    get pagerank value
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: node id and pagerank value
    
    """
    pagerank_value = centrality.PageRank(net, damp=0.85, tol=1e-9)
    pagerank_value.run()
    pagerank_file = outpath + label + '-pagerank-falseid-value'
    nodes_id, pagerank_values = zip(*pagerank_value.ranking())
    pagerank_ranking = open(pagerank_file, 'w')
    for i in range(len(nodes_id)):
        pagerank_ranking.write(str(nodes_id[i]) + '\t' + str(pagerank_values[i]) + '\n')
    pagerank_ranking.close()
    return nodes_id, pagerank_values


def get_cc_centrality_distr(centrality_filename):
    """
    get complementary cumulative centrality distribution

    :param centrality_filename: centrality filename

    :return: unique value and ccdf

    """
    centrality_file = open(centrality_filename, 'r')
    val = []
    while True:
        line = centrality_file.readline()
        if not line:
            break
        splited_line = line.strip().split('\t')
        val.append(float(splited_line[1]))
    centrality_file.close()
    unique_val, unique_cnt = np.unique(val, return_counts=True)
    tmp_sum = sum(unique_cnt)
    # unique_cc_cnt = [sum(unique_cnt[i:]) / tmp_sum for i in range(len(unique_cnt))]
    unique_cc_cnt = tmp_sum - np.cumsum(unique_cnt) + unique_cnt
    unique_cc_prob = unique_cc_cnt / tmp_sum
    return unique_val, unique_cc_prob


def get_hop_distr(net, label, outpath):
    """
    get hop distribution
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: distance and proportion
    
    """
    hop_appro = distance.HopPlotApproximation(net)
    hop_appro.run()
    hop_dist = hop_appro.getHopPlot()
    dist = []
    proportion = []
    for d in sorted(hop_dist):
        dist.append(d)
        proportion.append(hop_dist[d])
    hop_file = open(outpath + label + "hop-distribution", 'w')
    for i in range(len(dist)):
        hop_file.write(str(dist[i]) + '\t' + str(proportion[i]) + '\n')
    hop_file.close()
    return dist, proportion


def get_lcc_subgraph(net):
    """
    get the largest connected component
    
    :param net: networkit graph object
    
    :return: subgraph induced by largest connected component
    
    """
    cc = components.ConnectedComponents(net)
    cc.run()
    partition = cc.getPartition()
    scc_size_map = partition.subsetSizeMap()
    lcc_size = 0
    lcc_id = 0
    for id in scc_size_map.keys():
        if scc_size_map[id] > lcc_size:
            lcc_size = scc_size_map[id]
            lcc_id = id
    print(lcc_id, lcc_size)
    lcc_index = list(partition.getMembers(lcc_id))
    result_subgraph = networkit.Graph.subgraphFromNodes(net, lcc_index)
    # print(result_sbgraph.numberOfNodes())
    # print(result_sbgraph.numberOfEdges())
    return result_subgraph


def get_lscc_subgraph(net):
    """
    get the largest strongly connected component

    :param net: networkit graph object
    
    :return: subgraph induced by largest strongly connected component

    """
    scc = components.StronglyConnectedComponents(net)
    scc.run()
    scc_partition = scc.getPartition()
    scc_size_map = scc_partition.subsetSizeMap()
    lscc_size = 0
    lscc_id = 0
    for id in scc_size_map.keys():
        if scc_size_map[id] > lscc_size:
            lscc_size = scc_size_map[id]
            lscc_id = id
    print(lscc_id, lscc_size)
    lscc_index = list(scc_partition.getMembers(lscc_id))
    print(len(lscc_index))
    result_subgraph = networkit.Graph.subgraphFromNodes(net, lscc_index)
    print(result_subgraph.numberOfNodes())
    print(result_subgraph.numberOfEdges())
    return result_subgraph


def write_map_node_id(net_reader, label, outpath):
    """
    write mapNodeId to file.
    
    :param net_reader: networkit reader object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: dict. key is real id in origin id pair file, and value is id used in program
    
    """
    out = open(outpath + label + '-map-node-ids', 'w')
    map_node_ids = networkit.graphio.EdgeListReader.getNodeMap(net_reader)
    for raw_id in map_node_ids:
        processed_id = map_node_ids[raw_id]
        out.write(str(raw_id) + '\t' + str(processed_id) + '\n')
    out.close()


def get_falseid_trueid_map(map_filename):
    """
    get node id map
    
    :param map_filename: map node id file
    
    :return: key is id used in program, and value is real id in origin id pair file
    
    """
    map_file = open(map_filename, 'r')
    result = dict()
    while True:
        line = map_file.readline()
        if not line:
            break
        split_line = line.strip().split(sep='\t')
        result[split_line[1]] = split_line[0]
    map_file.close()
    return result


def get_average_shortest_path_appro(connected_net, sample_num):
    """
    estimate average shortest path.
    
    subgraph bug! why does subgraph store unnecessary information of origin graph? BFS can detect this bug. 
    
    :param connected_net: connected graph
    
    :param sample_num: sample size. the larger the number is,  the slower the program is.
    
    :return: approximately average shortest path
    
    """
    sample = []
    nodes = connected_net.nodes()
    for i in range(sample_num):
        sample.append(nodes[random.randint(1, len(nodes))])
    sampled_path_length = 0

    for source in sample:
        bfs = distance.BFS(connected_net, source=source, storePaths=False)
        bfs.run()
        for target in nodes:
            sampled_path_length = sampled_path_length + bfs.distance(target)
    result = sampled_path_length / (len(sample) * len(nodes))
    return result


def falseid_to_trueid(false_id_list, map_filename):
    """
    transfer id to name

    :param false_id_list: false id list

    :param map_filename: map filename. In this map file, the first column is true id and the second column is false id.

    :return: true id list

    """
    map_file = open(map_filename, 'r')
    id_name_map = dict()
    while True:
        line = map_file.readline()
        if not line:
            break
        splited_line = line.strip().split('\t')
        id_name_map[splited_line[1]] = splited_line[0]
    map_file.close()
    trueid_list = []
    for id in false_id_list:
        trueid = id_name_map.get(id)
        trueid_list.append(trueid)
    return trueid_list


def trueid_to_name(id_list, index_filename):
    """
    transfer id to name

    :param id_list: true id list

    :param index_filename: index filename

    :return: name list

    """
    index_file = open(index_filename, 'r')
    id_name_map = dict()
    while True:
        line = index_file.readline()
        if not line:
            break
        splited_line = line.strip().split('\t')
        id_name_map[splited_line[0]] = splited_line[1]
    index_file.close()
    name_list = []
    for id in id_list:
        name = id_name_map.get(id)
        name_list.append(name)
    return name_list


if __name__ == '__main__':
    filepath = '/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/YAGO3/facts-id-pair'
    label = "facts-id-pair"
    outpath = './output/' + label + '/'
    # net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    # get_deg_dist(net)
    # get_cc_deg_dist(net, degree_type='all')
    # shortest_distances =distance.APSP(net)
    # shortest_distances.run()
    # shortest_distances.getDistances()
    # print(shortest_distances)

    # filepath = "./input/NELL/nell-all-id-pair"
    # net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    # subgraph = get_lcc_subgraph(net)
    # avg_shortest_path = get_average_shortest_path_appro(subgraph, 1)
    # print(avg_shortest_path)

    # write degree to file
    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=False)
    net = net_reader.read(filepath)
    write_map_node_id(net_reader, label, outpath + 'undirected-')
    get_and_write_deg_dist(net, label, outpath, degree_type='all')

    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=True)
    net = net_reader.read(filepath)
    write_map_node_id(net_reader, label, outpath + 'directed-')
    get_and_write_deg_dist(net, label, outpath, degree_type='in')
    get_and_write_deg_dist(net, label, outpath, degree_type='out')
