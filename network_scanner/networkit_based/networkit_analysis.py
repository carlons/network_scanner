import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append('../')
import logging
import networkit
from networkit import *
import os
import numpy as np
import network_scanner.networkit_based.networkit_util as networkit_util
import network_scanner.networkit_based.networkit_plot as networkit_plot


def analysis_undirected(net, label, outpath):
    """
    analysis undirected network
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: None
    
    """
    # check whether the graph is undirected
    is_directed = net.isDirected()
    if is_directed:
        logging.error('input graph should be undirected')
    else:
        logging.info('Undirected graph')

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # 基本信息
    #  profile
    nodes = net.numberOfNodes()
    edges = net.numberOfEdges()
    logging.info('number of nodes: {0}'.format(nodes))
    logging.info('number of edges: {0}'.format(edges))
    pf = profiling.Profile.create(net, preset="minimal")
    pf.output("HTML", outpath)
    # os.rename(outpath+label+'.html', outpath+label+'-undirected.html')
    logging.info('\n')

    # 度分布
    logging.info('write degree to file...')
    networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='all')
    logging.info('start to plot degree distribution...')
    uniqe_deg_seq = networkit_plot.plot_degree_dist(net, label, outpath)
    logging.info('min degree: {0}'.format(min(uniqe_deg_seq)))
    logging.info('max degree: {0}'.format(max(uniqe_deg_seq)))
    logging.info('average degree: {0}'.format(2*edges/nodes))
    logging.info('\n')

    # 补累积度分布
    logging.info('start to plot complementary cumulative (in/out) degree distribution...')
    networkit_plot.plot_ccum_degree_dist(net, label, outpath, degree_type='all')
    logging.info('plot cc degree distribution done.\n')

    # 聚类系数
    # global clustering coefficient. The first definition in http://konect.uni-koblenz.de/statistics/clusco
    logging.info('calculating clustering coefficient...')
    global_cc = globals.ClusteringCoefficient.approxGlobal(net, nodes)
    logging.info('approximate clustering coefficient: {0}'.format(global_cc))
    logging.info('')
    logging.info('plot cumulative distribution of local clustering coefficient...')
    networkit_plot.plot_cum_clustering_dist(net, label, outpath, turbo=True)
    logging.info('plot local clustering coefficient done.\n')
    # The second definition in http://konect.uni-koblenz.de/statistics/clusco.
    # cc = globals.clustering(net, error=0.01)
    # print("clustering coefficient ", cc)

    # 连通分支
    # connected components
    logging.info('plot connected components...')
    connected_components = networkit_plot.plot_connected_component_dist(net, label, outpath)
    logging.info('number of connected components: {0}'.format(len(connected_components)))
    lcc = np.max(connected_components)
    logging.info('largest connected component size: {0}'.format(lcc))
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('lcc nodes percentage: {0}'.format(lcc_subgraph.numberOfNodes() / net.numberOfNodes()))
    logging.info('lcc edges percentage: {0}'.format(lcc_subgraph.numberOfEdges() / net.numberOfEdges()))
    logging.info('components done.\n')

    # eigenvector centrality
    logging.info('calculating eigenvector centrality...')
    networkit_plot.plot_eigenvector_centrality(net, label, outpath)
    centrality_name = 'eigenvector-centrality'
    centrality_filename = outpath + label + '-' + centrality_name + '-falseid-value'
    paras = {'centrality_filename': centrality_filename, 'label': label, 'outpath': outpath,
             'centrality_name': centrality_name}
    networkit_plot.plot_ccum_centrality_dist(**paras)
    logging.info('eigenvector centrality done.\n')

    # 距离, 只支持无向图. 有效直径只支持无向连通图.
    # distance
    logging.info('calculating diameter...')
    diameter = distance.Diameter(net)
    diameter.run()
    logging.info('diameter: {0}'.format(diameter.getDiameter()))
    logging.info('\n')
    # effective diameter now only undirected connected graph
    logging.info('calculating effective diameter...')
    eff_diameter = distance.EffectiveDiameterApproximation(lcc_subgraph, ratio=0.9)
    eff_diameter.run()
    logging.info('effective diameter: {0}'.format(eff_diameter.getEffectiveDiameter()))
    logging.info('distance done.\n')

    # 依据度的同配混合
    logging.info('calculating assorsativity...')
    assorsativity = networkit_util.get_assorsativity(net)
    logging.info('assorsativity: {0}'.format(assorsativity))
    logging.info('plot assorsativity...')
    networkit_plot.plot_assorsativity(net, label, outpath, degree_type='all')
    logging.info('assorsativity done\n')


def analysis_directed(net, label, outpath):
    """
    analysis directed network
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: None
    
    """
    # check whether graph is directed
    is_directed = net.isDirected()
    if not is_directed:
        logging.error('input grapg should be directed.')
    else:
        logging.info('Directed graph')

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # 基本信息
    #  profile
    nodes = net.numberOfNodes()
    edges = net.numberOfEdges()
    logging.info('number of nodes: {0}'.format(nodes))
    logging.info('number of edges: {0}'.format(edges))
    pf = profiling.Profile.create(net, preset="minimal")
    pf.output("HTML", outpath)
    # os.rename(outpath+label+'.html', outpath+label+'-directed.html')
    logging.info('\n')

    # 入度分布
    logging.info('write indegree to file...')
    networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='in')
    logging.info('start to plot in-degree distribution...')
    uniqe_deg_seq = networkit_plot.plot_indeg_dist(net, label, outpath)
    logging.info('min in-degree: {0}'.format(min(uniqe_deg_seq)))
    logging.info('max in-degree: {0}'.format(max(uniqe_deg_seq)))
    logging.info('\n')

    # 出度分布
    logging.info('write outdegree to file...')
    networkit_util.get_and_write_deg_dist(net, label, outpath, degree_type='out')
    logging.info('start to plot out-degree distribution...')
    uniqe_deg_seq = networkit_plot.plot_outdeg_dist(net, label, outpath)
    logging.info('min out-degree: {0}'.format(min(uniqe_deg_seq)))
    logging.info('max out-degree: {0}'.format(max(uniqe_deg_seq)))
    logging.info('\n')

    # 补累积(入/出)度分布
    logging.info('start to plot complementary cumulative (in/out) degree distribution...')
    networkit_plot.plot_ccum_degree_dist(net, label, outpath, degree_type='in')
    networkit_plot.plot_ccum_degree_dist(net, label, outpath, degree_type='out')
    logging.info('plot cc (in/out) degree distribution done.\n')

    # 出度/入度联合分布
    logging.info('plot outdegree vs indegree...')
    networkit_plot.plot_out_in_degree_comparision(net, label, outpath)
    logging.info('plot out vs in done.\n')

    # 相互性
    # reciprocity
    logging.info('calculating reciprocity...')
    reciprocity = networkit_util.get_reciprocity(net)
    logging.info('reciprocity: {0}'.format(reciprocity))
    logging.info('reciprocity done.\n')

    # 连通分支
    # weakly connected components
    logging.info('plot wcc distribution...')
    wcc = networkit_plot.plot_wcc_dist(net, label, outpath)
    logging.info('number of weakly connected components: {0}'.format(len(wcc)))
    lwcc = np.max(wcc)
    logging.info('largest weakly connected component size: {0}'.format(lwcc))
    logging.info('')
    # strongly connected components
    logging.info('plot scc distribution...')
    scc = networkit_plot.plot_scc_dist(net, label, outpath)
    logging.info('number of strongly connected components: {0}'.format(len(scc)))
    lscc = np.max(scc)
    logging.info('largest strongly connected component size: {0}'.format(lscc))
    lscc = networkit_util.get_lscc_subgraph(net)
    logging.info('lcc nodes percentage: {0}'.format(lscc.numberOfNodes() / net.numberOfNodes()))
    logging.info('lcc edges percentage: {0}'.format(lscc.numberOfEdges() / net.numberOfEdges()))
    logging.info('components done.\n')

    # Pagerank
    logging.info('calculating pagerank...')
    networkit_plot.plot_pagerank(net, label, outpath)
    centrality_name = 'pagerank'
    centrality_filename = outpath + label + '-' + centrality_name + '-falseid-value'
    paras = {'centrality_filename': centrality_filename, 'label': label, 'outpath': outpath,
             'centrality_name': centrality_name}
    networkit_plot.plot_ccum_centrality_dist(**paras)
    logging.info('pagerank done.\n')


def analysis(filepath, label, outpath, directed=False):
    """
    analysis

    :return: None 

    """
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    if not directed:
        # set logging
        # I guess there exists conflict. So add code below.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        log_filepath = outpath + label + '-undirected.log'
        logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        logging.info('read graph from file')
        net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=False)
        net = net_reader.read(filepath)
        logging.info('get undirected map node id...')
        networkit_util.write_map_node_id(net_reader, label, outpath + 'undirected-')
        logging.info('******************************************')
        paras = {'net': net, 'label': label, 'outpath': outpath}
        analysis_undirected(**paras)
        logging.info('******************************************')
        logging.info('done ^-^')
    if directed:
        # set logging
        # I guess there exists conflict. So add code below.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        log_filepath = outpath + label + '-directed.log'
        logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=True)
        net = net_reader.read(filepath)
        logging.info('get directed map node id...')
        networkit_util.write_map_node_id(net_reader, label, outpath + 'directed-')
        paras = {'net': net, 'label': label, 'outpath': outpath}
        analysis_directed(**paras)
        logging.info('done ^-^')