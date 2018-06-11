import matplotlib
matplotlib.use('Agg')
import logging
import networkit
from networkit import *
import os
import network_scanner.networkit_based.networkit_plot as networkit_plot


def get_exact_clustering_coefficient(net, label, outpath):
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
    log_filepath = outpath + label + label + '_exact-clustering-coefficient.log'
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
    # global clustering coefficient. The first definition in http://konect.uni-koblenz.de/statistics/clusco
    logging.info('calculating clustering coefficient...')
    global_cc = globals.ClusteringCoefficient.exactGlobal(net)
    logging.info('clustering coefficient: {0}'.format(global_cc))
    logging.info('')
    logging.info('plot cumulative distribution of local clustering coefficient...')
    networkit_plot.plot_cum_clustering_dist(net, label, outpath, turbo=False)
    logging.info('plot local clustering coefficient done.\n')


def get_appro_clustering_coefficient(net, label, outpath):
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
    log_filepath = outpath + label + label + '_appro-clustering-coefficient.log'
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
    # global clustering coefficient. The first definition in http://konect.uni-koblenz.de/statistics/clusco
    logging.info('calculating clustering coefficient...')
    global_cc = globals.ClusteringCoefficient.approxGlobal(net, net.numberOfNodes())
    logging.info('clustering coefficient: {0}'.format(global_cc))
    logging.info('')
    logging.info('plot cumulative distribution of local clustering coefficient...')
    networkit_plot.plot_cum_clustering_dist(net, label, outpath, turbo=True)
    logging.info('plot local clustering coefficient done.\n')