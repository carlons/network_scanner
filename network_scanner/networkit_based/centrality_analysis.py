import numpy as np
import scipy
import matplotlib
import mpmath
import os
import powerlaw
from matplotlib import pyplot as plt
import logging
import network_scanner.networkit_based.networkit_util as networkit_util


def get_top_k_id(centrality_filename, map_filename, k):
    """
    get top k's id
    
    :param centrality_file: centrality filename
    
    :param map_filename: map filename
    
    :param k: number
    
    :return: top k id
    
    """
    centrality_file = open(centrality_filename, 'r')
    id_map = networkit_util.get_falseid_trueid_map(map_filename)
    top_k_id = []
    cnt = 0
    while True:
        line = centrality_file.readline()
        if not line:
            break
        cnt = cnt + 1
        splited_line = line.strip().split('\t')
        top_k_id.append(id_map.get(splited_line[0]))
        if cnt >= k:
            break
    centrality_file.close()
    return top_k_id


def get_top_k_name(top_k_id, index_filename):
    """
    get top k's name from index file
    
    :param top_k_id: top k id
    
    :param index_filename: index filename
    
    :return: top k name
    
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
    top_k_name = []
    for id in top_k_id:
        name = id_name_map.get(id)
        top_k_name.append(name)
    return top_k_name


def get_centrality_seq(centrality_filename):
    """
    get centrality sequence
    
    :param centrality_filename: centrality filename
    
    :return: centrality value
    
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
    return val


def power_law_analysis(centrality_filename, centrality_name, label, outpath):
    """
    analysis power law
    
    :param centrality_filename: centrality filename

    :param centrality_name: centrality name

    :param label: network label
    
    :param outpath: output directory
    
    :return: None
    
    """
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + label + '_' + centrality_name + '_powerlaw.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                      'message)s', level=logging.INFO)

    data = get_centrality_seq(centrality_filename)
    fit = powerlaw.Fit(data, discrete=False)
    logging.info('power law fit result:')
    logging.info('Is discrete: {0}'.format(fit.estimate_discrete))
    logging.info('x_min = {0}'.format(fit.xmin))
    logging.info('power_law_alpha = {0}'.format(fit.power_law.alpha))
    logging.info('power_law_D = {0}'.format(fit.power_law.D))
    logging.info('\n')

    R1, p1 = fit.distribution_compare('power_law', 'exponential')
    logging.info('Compare with exponential:')
    logging.info('R = {0}'.format(R1))
    logging.info('p = {0}'.format(p1))
    logging.info('\n')

    R2, p2 = fit.distribution_compare('power_law', 'truncated_power_law')
    logging.info('Compare with truncated power law:')
    logging.info('R = {0}'.format(R2))
    logging.info('p = {0}'.format(p2))
    logging.info('\n')

    R3, p3 = fit.distribution_compare('power_law', 'lognormal')
    logging.info('Compare with lognormal:')
    logging.info('R = {0}'.format(R3))
    logging.info('p = {0}'.format(p3))
    logging.info('\n')

    R4, p4 = fit.distribution_compare('power_law', 'stretched_exponential')
    logging.info('Compare with stretched exponential:')
    logging.info('R = {0}'.format(R4))
    logging.info('p = {0}'.format(p4))
    logging.info('\n')

    logging.info('Truncated power law fit result: ')
    logging.info('{0} = {1}'.format(fit.truncated_power_law.parameter1_name, fit.truncated_power_law.parameter1))
    logging.info('{0} = {1}'.format(fit.truncated_power_law.parameter2_name, fit.truncated_power_law.parameter2))
    logging.info('\n')

    logging.info('Lognormal fit result: ')
    logging.info('{0} = {1}'.format(fit.lognormal.parameter1_name, fit.lognormal.parameter1))
    logging.info('{0} = {1}'.format(fit.lognormal.parameter2_name, fit.lognormal.parameter2))

    ####
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fit.plot_ccdf(color='c', linewidth=2, ax=ax)
    fit.power_law.plot_ccdf(color='c', linestyle='--', ax=ax)
    ####
    ax.set_ylabel(u"p(X≥x)")
    ax.set_xlabel(u"x")

    figname = outpath + label + '-powerlaw'
    plt.savefig(figname + '.eps', bbox_inches='tight')


if __name__ == '__main__':
    # base_centrality_path = '/home/carlons/workspace_python/network_data_analysis/snap_based/output/'
    base_centrality_path = './output/'
    centrality_filename = base_centrality_path + 'probase-id-pair/probase-id-pair-pagerank-top100'
    # base_index_path = '/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/'
    # index_filename = base_index_path + 'Probase/probase-index'
    map_filename = './output/probase-id-pair/probase-id-pair-map-node-ids'
    k = 10
    top_k_id = get_top_k_id(centrality_filename, map_filename, k)
    print(top_k_id)
    # top_k_name = get_top_k_name(top_k_id, index_filename)
    # for name in top_k_name:
    #     print(name, ' \\\\')