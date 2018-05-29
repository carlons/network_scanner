import networkit
from networkit import *
import sys
sys.path.append('../')
import networkit_based.degree_analysis
import networkit_based.centrality_analysis

if __name__ == '__main__':
    # filepath = '../knowledge_graph/output/DBpedia/mappingbased_id_pair'
    # label = 'mappingbased_id_pair'
    # outpath = './output/' + label + '/'
    # net = networkit.graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'all')
    # net = networkit.graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False,
    #                                   directed=True)
    # print('degree done')
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'in')
    # print('in degree done')
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'out')
    # print('out degree done')
    #
    # degree_type = {'all': 'all', 'in': 'in', 'out': 'out'}
    # for item in degree_type:
    #     new_label = label + '-' + item + '-degree'
    #     filepath = outpath + new_label
    #
    #     # set logging
    #     # I guess there exists conflict. So add code below.
    #     for handler in logging.root.handlers[:]:
    #         logging.root.removeHandler(handler)
    #     log_filepath = outpath + new_label + '-power-law.log'
    #     logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(''message)s', level=logging.INFO)
    #
    #     networkit_based.degree_analysis.power_law_analysis(filepath, new_label, outpath, item)

    filepath = '../snap_based/output/mappingbased_id_pair/mappingbased_id_pair-pagerank'
    label = 'mappingbased_id_pair'
    outpath = '../snap_based/output/' + label + '/'
    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + '-pagerank-power-law.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(''message)s', level=logging.INFO)

    networkit_based.centrality_analysis.power_law_analysis(filepath, label + '-pagerank', outpath)