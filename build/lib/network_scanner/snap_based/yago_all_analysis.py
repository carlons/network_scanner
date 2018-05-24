import sys
# sys.path.append('/home/amax/Hxk/workspace_py/network_data_analysis')
sys.path.append('../')
import snap_based.centrality_plot
# import snap
# import snap_based.centrality_analysis
# import os

if __name__ == '__main__':
    # parameters
    # filepath = "../input/YAGO3/taxonomy-types-facts-id-pair"
    # label = "taxonomy-types-facts-id-pair"
    # outpath = './output/' + label + '/'

    # check whether the output directory exists
    # if not os.path.exists(outpath):
    #    os.mkdir(outpath)
    # net = snap.LoadEdgeList(snap.PNGraph, filepath, 0, 1)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # snap_based.centrality_analysis.get_pagerank(**paras)
    # print('pagerank done')
    # snap_based.centrality_analysis.get_hits(**paras)
    # print('HITS done')
    # net = snap.LoadEdgeList(snap.PUNGraph, filepath, 0, 1)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # snap_based.centrality_analysis.get_eigen_vector_centr(**paras)
    # snap_based.centrality_analysis.get_betweenness_centr(**paras)
    # print('done')
    filename = './output/taxonomy-types-facts-id-pair/taxonomy-types-facts-id-pair-'
    label = 'taxonomy-types-facts-id-pair-'
    outpath = './output/taxonomy-types-facts-id-pair/'
    centrality_name = ['eigen_vector_centr', 'pagerank', 'hub', 'authority']
    for name in centrality_name:
        paras = {'centrality_filename': filename + name, 'label': label + name, 'outpath': outpath, 'centrality_name': name}
        snap_based.centrality_plot.plot_ccum_centrality_dist(**paras)