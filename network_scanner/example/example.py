import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import network_scanner
import logging
import os
import networkit
from network_scanner.networkit_based import degree_analysis
from network_scanner.networkit_based import calculate_betweeness
from network_scanner.networkit_based import centrality_analysis
from network_scanner.networkit_based import networkit_util
from network_scanner.networkit_based import networkit_analysis
from network_scanner.networkit_based import networkit_plot


if __name__ == '__main__':
    filepath = './input/toy_graph'
    label = 'toy'
    outpath = './output/' + label + '/'
    
    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    
    # 1. general analysis
    networkit_analysis.analysis(filepath, label, outpath, directed=False)
    networkit_analysis.analysis(filepath, label, outpath, directed=True)

    # 3. distance analysis
    # set logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + 'distance.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %('
                                                                              'message)s', level=logging.INFO)
    # start
    net = networkit_util.readnetwork(filepath, directed=False)
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('plot hop...')
    paras = dict(net=lcc_subgraph, label=label, outpath=outpath)
    networkit_plot.plot_hop_dist(**paras)
    logging.info('')
    logging.info('estimate average shortest path')
    sample_num = 100
    logging.info('sample size: {0}'.format(sample_num))
    asp = networkit_util.get_average_shortest_path_appro(lcc_subgraph, sample_num=sample_num)
    logging.info('estimated average shortest path: {0}'.format(asp))

    # 5. calculate betweeness. 
    net = networkit_util.readnetwork(filepath, directed=False)
    calculate_betweeness.get_betweeness(net, label, outpath)

    # 6. centrality analysis
    # pagerank_filename = outpath + label + '-pagerank-falseid-value'
    # map_filename = outpath + 'directed-' + label + '-map-node-ids'
    # index_filename = './input/index'
    # top_k_filename = outpath + label + '-pagerank-top-name'
    # k = 100
    # top_k_list = centrality_analysis.get_top_k_id(pagerank_filename, map_filename, 100)
    # top_k_name = centrality_analysis.get_top_k_name(top_k_list, index_filename)
    # top_k_file = open(top_k_filename, 'w')
    # for item in top_k_name:
    #     top_k_file.write(str(item) + '\n')
    # top_k_file.close()

    # 2. degree analysis
    # false_id_value_filename = outpath + 'toy-falseid-degree'
    # map_filename = outpath + 'undirected-toy-map-node-ids'
    # index_filename = './input/index'
    # result_filename = outpath + label + 'degree-top-k-trueid-value'
    # k = 3
    # paras = {'false_id_value_filename': false_id_value_filename, 'map_filename': map_filename,
    #          'index_filename': index_filename, 'result_filename': result_filename, 'k': k}
    # degree_analysis.get_top_k_trueid_and_name(**paras)
    # net = networkit_util.readnetwork(filepath, directed=False)
    # degree_analysis.get_deg_seq(net, label, outpath, degree_type='all')
    # degree_seq_filename = outpath + 'toy-all-degree'
    # degree_analysis.power_law_analysis(degree_seq_filename, label, outpath, degree_type='all')
    #     indeg_falseid_value_filename = outpath + 'toy-falseid-indegree'
    #     outdeg_falseid_value_filename = outpath + 'toy-falseid-outdegree'
    #     map_filename = outpath + 'directed-toy-map-node-ids'
    #     index_filename = './input/index'
    #     result_filename = outpath + label + 'indeg-vs-outdeg'
    #     paras = {'indeg_falseid_value_filename': indeg_falseid_value_filename,
    #              'outdeg_falseid_value_filename': outdeg_falseid_value_filename, 'map_filename': map_filename,
    #               'index_filename': index_filename, 'result_filename': result_filename}
    
    # 4. calculate exact clustering coefficient
    # net = networkit_util.readnetwork(filepath, directed=False)
    # calculate_clustering_coefficient.get_exact_clustering_coefficient(net, label, outpath)
