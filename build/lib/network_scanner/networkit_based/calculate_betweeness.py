import matplotlib
matplotlib.use('Agg')
import logging
import networkit
from networkit import *
import os
import network_scanner.networkit_based.networkit_util as networkit_util
import network_scanner.networkit_based.networkit_plot as networkit_plot


def get_betweeness(net, label, outpath):
    """
    analysis undirected network
    
    :param net: networkit graph pbject
    
    :param label: network label
    
    :param outpath: result output directory
    
    :return: None
    
    """
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + label + '_betweeness.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                      'message)s', level=logging.INFO)

    # check whether the graph is undirected
    is_directed = net.isDirected()
    if is_directed:
        logging.error('input graph should be undirected')
    else:
        logging.info('Undirected graph')

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # time-consuming
    logging.info('calculating betweeness...')
    networkit_plot.plot_betweeness(net, label, outpath)
    centrality_name = 'betweeness'
    centrality_filename = outpath + label + '-' + centrality_name + '-falseid-value'
    paras = {'centrality_filename': centrality_filename, 'label': label, 'outpath': outpath,
             'centrality_name': centrality_name}
    networkit_plot.plot_ccum_centrality_dist(**paras)
    logging.info('done')


def main():
    """
    function entrance
    
    :return: None
    
    """
    # parameters
    filepath = '/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/DBpedia/mappingbased_id_pair'
    label = "mappingbased_id_pair"
    outpath = './output/' + label + '/'

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + label + '_betweeness.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                                          'message)s', level=logging.INFO)

    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=False)
    net = net_reader.read(filepath)
    # net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    paras = {'net': net, 'label': label, 'outpath': outpath}
    networkit_util.write_map_node_id(net_reader, label, outpath)
    logging.info('write map node id to file...')
    get_betweeness(**paras)
    logging.info('******************************************')
    logging.info('done ^-^')


if __name__ == '__main__':
    main()
