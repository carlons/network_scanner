import network_scanner
from network_scanner.networkit_based import degree_analysis
from network_scanner.networkit_based import calculate_betweeness
from network_scanner.networkit_based import centrality_analysis
from network_scanner.networkit_based import networkit_util
from network_scanner.networkit_based import networkit_analysis


if __name__ == '__main__':
    filepath = './input/toy_graph'
    label = 'toy'
    outpath = './output/' + label + '/'

    # test networkit_analysis
    # networkit_analysis.analysis(filepath, label, outpath, directed=False)
    # networkit_analysis.analysis(filepath, label, outpath, directed=True)

    # test calculate_betweeness
    # net = networkit_util.readnetwork(filepath, directed=False)
    # calculate_betweeness.get_betweeness(net, label, outpath)

    # test centrality_analysis
    # pagerank_filename = outpath + 'toy-pagerank-falseid-value'
    # map_filename = outpath + 'directed-toy-map-node-ids'
    # top_k_list = centrality_analysis.get_top_k_id(pagerank_filename, map_filename, 3)
    # print(top_k_list)
    # index_filename = './input/index'
    # top_k_name = centrality_analysis.get_top_k_name(top_k_list, index_filename)
    # print(top_k_name)
    # centrality_analysis.power_law_analysis(pagerank_filename, 'pagerank', label, outpath)

    # test degree_analysis
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
    indeg_falseid_value_filename = outpath + 'toy-falseid-indegree'
    outdeg_falseid_value_filename = outpath + 'toy-falseid-outdegree'
    map_filename = outpath + 'directed-toy-map-node-ids'
    index_filename = './input/index'
    result_filename = outpath + label + 'indeg-vs-outdeg'
    paras = {'indeg_falseid_value_filename': indeg_falseid_value_filename,
             'outdeg_falseid_value_filename': outdeg_falseid_value_filename, 'map_filename': map_filename,
              'index_filename': index_filename, 'result_filename': result_filename}
