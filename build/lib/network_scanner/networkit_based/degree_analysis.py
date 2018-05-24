import numpy as np
import scipy
import matplotlib
import mpmath
import powerlaw
from matplotlib import pyplot as plt
import logging


def get_deg_seq(net, label, outpath, degree_type):
    """
    get and store degree sequence
    
    :param net: networkit graph object
    
    :param label: network label
    
    :param outpath: figure output directory
    
    :param degree_type: all, in, out
    
    :return: None
    
    """
    if degree_type not in ['all', 'in', 'out']:
        print("ERROR degree type.")
        return
    outfile = open(outpath + label + '-' + degree_type + '-degree', 'w')
    ret = []
    if degree_type == 'all':
        ret = [net.degree(node) for node in net.nodes()]
    if degree_type == 'in':
        ret = [net.degreeIn(node) for node in net.nodes()]
    if degree_type == 'out':
        ret = [net.degreeOut(node) for node in net.nodes()]
    for ele in ret:
        outfile.write(str(ele) +'\n')
    outfile.close()


def power_law_analysis(filename, label, outpath, degree_type):
    """
    analysis power law
      
    :param filename: degree sequence filename
      
    :param label: network label
    
    :param outpath: output directory
    
    :param degree_type: all, in, out
      
    :return: None
    
    """
    data = np.genfromtxt(filename)
    fit = powerlaw.Fit(data, discrete=True)
    logging.info('power law fit result:')
    logging.info('Is discrete: {0}'.format(fit.estimate_discrete))
    logging.info('x_min = {0}'.format(fit.xmin))
    logging.info('power_law_alpha = {0}'.format(fit.power_law.alpha))
    logging.info('power_law_D = {0}'.format(fit.power_law.D))
    logging.info('\n')

    R1, p1 = fit.distribution_compare('power_law', 'exponential')
    logging.info('Compare with exponential:')
    logging.info('R = {0}'.format(R1))
    logging.info('p = {0}'.format(p1))
    logging.info('\n')

    R2, p2 = fit.distribution_compare('power_law', 'truncated_power_law')
    logging.info('Compare with truncated power law:')
    logging.info('R = {0}'.format(R2))
    logging.info('p = {0}'.format(p2))
    logging.info('\n')

    R3, p3 = fit.distribution_compare('power_law', 'lognormal')
    logging.info('Compare with lognormal:')
    logging.info('R = {0}'.format(R3))
    logging.info('p = {0}'.format(p3))
    logging.info('\n')

    R4, p4 = fit.distribution_compare('power_law', 'stretched_exponential')
    logging.info('Compare with stretched exponential:')
    logging.info('R = {0}'.format(R4))
    logging.info('p = {0}'.format(p4))
    logging.info('\n')

    logging.info('Truncated power law fit result: ')
    logging.info('{0} = {1}'.format(fit.truncated_power_law.parameter1_name, fit.truncated_power_law.parameter1))
    logging.info('{0} = {1}'.format(fit.truncated_power_law.parameter2_name, fit.truncated_power_law.parameter2))
    logging.info('\n')

    logging.info('Lognormal fit result: ')
    logging.info('{0} = {1}'.format(fit.lognormal.parameter1_name, fit.lognormal.parameter1))
    logging.info('{0} = {1}'.format(fit.lognormal.parameter2_name, fit.lognormal.parameter2))

    ####
    color_type = {'all': 'b', 'in': 'g', 'out': 'c'}
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fit.plot_ccdf(color=color_type[degree_type], linewidth=2, ax=ax)
    fit.power_law.plot_ccdf(color=color_type[degree_type], linestyle='--', ax=ax)
    ####
    ax.set_ylabel(u"p(X≥x)")
    ax.set_xlabel(u"x")

    figname = outpath + label + '-powerlaw'
    plt.savefig(figname + '.eps', bbox_inches='tight')


if __name__ == '__main__':
    filename = ''
    label = ''
    outpath = ''
    # set logging
    # I guess there exists conflict. So add code below.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    log_filepath = outpath + label + '-power-law.log'
    logging.basicConfig(filename=log_filepath, format='%(asctime)s - %(levelname)s - %(''message)s', level=logging.INFO)



