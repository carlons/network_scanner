import network_scanner.networkit_based.networkit_analysis as network_analysis


def test():
    # parameters
    filepath = "./input/toy_graph"
    label = "toy_graph"
    outpath = './output/' + label + '/'
    directed = True

    paras = {'filepath': filepath, 'label': label, 'outpath': outpath, 'directed': directed}
    network_analysis.analysis(**paras)

if __name__ == '__main__':
    test()