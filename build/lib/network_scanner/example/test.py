import networkit
from networkit import *
import networkit_based.networkit_plot
import networkit_based.networkit_util
if __name__ == '__main__':
    filepath = '../input/Test/toy_graph'
    # net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=1, continuous=False, directed=False)
    net_reader = networkit.graphio.EdgeListReader(separator='\t', firstNode=1, continuous=False, directed=False)
    net = net_reader.read(filepath)
    print(net.nodes())
    print(net.numberOfNodes())
    print(net.edges())
    map_node_ids = networkit.graphio.EdgeListReader.getNodeMap(net_reader)
    networkit_based.networkit_util.write_map_node_id(net_reader, 'test', './output/')

    # filepath = "/home/carlons/workspace_python/network_data_analysis/knowledge_graph/output/NELL/nell-all-id-pair"
    # label = "nell-all-id-pair"
    # outpath = label + '/'
    # check whether the output directory exists
    # if not os.path.exists(outpath):
    #     os.mkdir(outpath)
    #
    # net = graphio.readGraph(filepath, Format.EdgeList, separator='\t', firstNode=1, continuous=True, directed=True)
    # paras = {'net': net, 'label': label, 'outpath': outpath}
    # networkit_based.networkit_plot.plot_pagerank(net, label, outpath)