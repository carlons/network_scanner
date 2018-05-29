import matplotlib.pyplot as plt
import numpy as np


def plot_ccum_centrality_dist(centrality_filename, label, outpath, centrality_name):
    """
    plot complementary cumulative centrality distribution
    :param centrality_filename:
    :param label:
    :param outpath:
    :return:
    """
    unique_val, unique_cc_prob = get_cc_centrality_distr(centrality_filename)
    centrality_style = {'eigen_vector_centr': 'c*', 'pagerank': 'g*', 'hub': 'r*', 'authority': 'm*'}
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(unique_val, unique_cc_prob, centrality_style[centrality_name], label=label)
    ax.set_xlabel('v')
    ax.set_ylabel('P(x>=v)')
    plt.savefig(outpath + label + '-distribution.eps')
    return ax


def get_cc_centrality_distr(centrality_filename):
    """
    get complementary cumulative centrality distribution
    :param centrality_filename:
    :return:
    """
    centrality_file = open(centrality_filename, 'r')
    val = []
    while True:
        line = centrality_file.readline()
        if not line:
            break
        splited_line = line.strip().split('\t')
        val.append(float(splited_line[1]))
    centrality_file.close()
    unique_val, unique_cnt = np.unique(val, return_counts=True)
    tmp_sum = sum(unique_cnt)
    # unique_cc_cnt = [sum(unique_cnt[i:]) / tmp_sum for i in range(len(unique_cnt))]
    unique_cc_cnt = tmp_sum - np.cumsum(unique_cnt) + unique_cnt
    unique_cc_prob = unique_cc_cnt / tmp_sum
    return unique_val, unique_cc_prob


if __name__ == '__main__':
    filename = './output/probase-id-pair/probase-id-pair-'
    label = 'probase-id-pair-'
    outpath = './output/probase-id-pair/'
    centrality_name = ['eigen_vector_centr', 'pagerank', 'hub', 'authority']
    for name in centrality_name:
        paras = {'centrality_filename': filename+name, 'label': label+name, 'outpath': outpath, 'centrality_name': name}
        plot_ccum_centrality_dist(**paras)