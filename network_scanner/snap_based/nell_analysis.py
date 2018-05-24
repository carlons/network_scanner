import snap
import os
import sys
# sys.path.append('/home/carlons/workspace_python/network_data_analysis/')
sys.path.append('/home/amax/Hxk/workspace_py/network_data_analysis')
import snap_based.centrality_analysis

if __name__ == '__main__':
    # parameters
    # filepath = '/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/NELL/nell-all-id-pair'
    filepath = "../input/NELL/nell-all-id-pair"
    label = "nell-all-id-pair"
    outpath = './output/' + label + '/'

    # check whether the output directory exists
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    # net = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # snap_based.centrality_analysis.get_pagerank(**paras)
    # print('pagerank done')
    # snap_based.centrality_analysis.get_hits(**paras)
    # print('HITS done')
    net = snap.LoadEdgeList(snap.PUNGraph, filepath, 0, 1)
    paras = {'net': net, 'label': label, 'outpath': outpath}
    # snap_based.centrality_analysis.get_eigen_vector_centr(**paras)
    snap_based.centrality_analysis.get_betweenness_centr(**paras)
    print('done')
