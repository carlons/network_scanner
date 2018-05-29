# import snap
import os
import sys
# sys.path.append('/home/carlons/workspace_python/network_data_analysis/')
# sys.path.append('/home/amax/Hxk/workspace_py/network_data_analysis')
# import snap_based.centrality_analysis
sys.path.append('../')
import snap_based.centrality_plot

if __name__ == '__main__':
    # # parameters
    # # filepath = '/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/YAGO3/facts-id-pair'
    # filepath = "../input/YAGO3/facts-id-pair"
    # label = "facts-id-pair"
    # outpath = './output/' + label + '/'
    #
    # # check whether the output directory exists
    # if not os.path.exists(outpath):
    #     os.mkdir(outpath)
    # # net = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    # # paras = {'net': net, 'label': label, 'outpath': outpath}
    # # snap_based.centrality_analysis.get_pagerank(**paras)
    # # print('pagerank done')
    # # snap_based.centrality_analysis.get_hits(**paras)
    # # print('HITS done')
    # net = snap.LoadEdgeList(snap.PUNGraph, filepath, 0, 1)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # # snap_based.centrality_analysis.get_eigen_vector_centr(**paras)
    # snap_based.centrality_analysis.get_betweenness_centr(**paras)
    # print('done')

    filename = './output/facts-id-pair/facts-id-pair-'
    label = 'facts-id-pair-'
    outpath = './output/facts-id-pair/'
    centrality_name = ['eigen_vector_centr', 'pagerank', 'hub', 'authority']
    for name in centrality_name:
        paras = {'centrality_filename': filename + name, 'label': label + name, 'outpath': outpath,
                 'centrality_name': name}
        snap_based.centrality_plot.plot_ccum_centrality_dist(**paras)