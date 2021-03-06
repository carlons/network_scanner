import logging
import network_scanner.networkit_based.networkit_util as networkit_util
import network_scanner.networkit_based.networkit_plot as networkit_plot
import networkit
from networkit import *


def plot_hop_dist(net, label, outpath):
    """
    plot hop distribution

    :param net: net

    :param label: label

    :param outpath: result path

    :return: None

    """
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + '-hop-distribution.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                      'message)s', level=logging.INFO)
    logging.info('get largest connected component...')
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('plot hop...')
    paras = dict(net=lcc_subgraph, label=label, outpath=outpath)
    networkit_plot.plot_hop_dist(**paras)
    logging.info('done.')


def estimate_average_shortest_path(net, label, outpath, sample_num):
    """
    estimate average shortest path length

    :param net: net

    :param label: label

    :param outpath: result path

    :param sample_num: sample number. the larger the sample_num is, the slower the program is.

    :return: None

    """
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + '-average-shortest-path.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                      'message)s', level=logging.INFO)
    logging.info('get largest connected component...')
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('sample size: {0}'.format(sample_num))
    asp = networkit_util.get_average_shortest_path_appro(lcc_subgraph, sample_num=sample_num)
    logging.info('estimated average shortest path: {0}'.format(asp))
    logging.info('done.')


def main():
    """
    plot hop distribution and estimate average shortest path length
    
    :return: None 
    
    """
    filepath = ''
    label = ''
    outpath = './output/' + label + '/'

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + '-distance.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                      'message)s', level=logging.INFO)

    logging.info('read graph')
    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=False)
    net = net_reader.read(filepath)
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('')
    logging.info('plot hop...')
    paras = dict(net=lcc_subgraph, label=label, outpath=outpath)
    networkit_plot.plot_hop_dist(**paras)
    logging.info('')
    logging.info('estimate average shortest path')
    sample_num = 100
    logging.info('sample size: {0}'.format(sample_num))
    asp = networkit_util.get_average_shortest_path_appro(lcc_subgraph, sample_num=sample_num)
    logging.info('estimated average shortest path: {0}'.format(asp))


if __name__ == '__main__':
    main()