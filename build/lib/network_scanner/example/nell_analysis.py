import networkit
from networkit import *
import sys
sys.path.append('../')
import networkit_based.degree_analysis
import networkit_based.centrality_analysis
import networkit_based.networkit_util

if __name__ == '__main__':
    filepath = '../knowledge_graph/output/NELL/nell-all-id-pair'
    label = 'nell-all-id-pair'
    outpath = './output/nell-all-id-pair/'
    net = networkit.graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False, directed=False)
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'all')
    # net = networkit.graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=0, continuous=False,
    #                                  directed=True)
    # print('degree done')
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'in')
    # print('in degree done')
    # networkit_based.degree_analysis.get_deg_seq(net, label, outpath, 'out')
    # print('out degree done')

    # degree_type = {'all': 'all', 'in': 'in', 'out': 'out'}
    # for item in degree_type:
    #     filepath = './output/nell-all-id-pair/nell-all-id-pair-' + item + '-degree'
    #     label = 'nell-all-id-pair-' + item + '-degree'
    #     outpath = './output/nell-all-id-pair/'
    #     # set logging
    #     # I guess there exists conflict. So add code below.
    #     for handler in logging.root.handlers[:]:
    #         logging.root.removeHandler(handler)
    #     log_filepath = outpath + label + '-power-law.log'
    #     logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(''message)s', level=logging.INFO)
    #
    #     networkit_based.degree_analysis.power_law_analysis(filepath, label, outpath, item)

    # pagerank power law
    # filepath = '../snap_based/output/nell-all-id-pair/nell-all-id-pair-pagerank'
    # label = 'nell-all-id-pair'
    # outpath = '../snap_based/output/' + label + '/'
    # # set logging
    # # I guess there exists conflict. So add code below.
    # for handler in logging.root.handlers[:]:
    #     logging.root.removeHandler(handler)
    # log_filepath = outpath + label + '-pagerank-power-law.log'
    # logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(''message)s', level=logging.INFO)
    #
    # networkit_based.centrality_analysis.power_law_analysis(filepath, label+'-pagerank', outpath)

    # effective diameter
    lcc_subgraph = networkit_based.networkit_util.get_lcc_subgraph(net)
    print('calculating effective diameter...')
    eff_diameter = distance.EffectiveDiameterApproximation(lcc_subgraph, ratio=0.9)
    eff_diameter.run()
    print(eff_diameter.getEffectiveDiameter())

    # hop plot
    # lcc_subgraph = networkit_based.networkit_util.get_lcc_subgraph(net)
    # hop_plot = distance.HopPlotApproximation(lcc_subgraph)
    # hop_plot.run()
    # result = hop_plot.getHopPlot()
    # print(result)