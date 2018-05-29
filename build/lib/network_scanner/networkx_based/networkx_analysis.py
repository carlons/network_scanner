import networkx as nx

if __name__ == '__main__':
    filepath = '../input/Test/toy_graph'
    net = nx.read_edgelist(filepath)
    print(nx.nodes(net))
    print(nx.edges(net))
    print(nx.pagerank(net))
