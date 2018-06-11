# Network Scanner

quick analysis network data based on [networkit](https://networkit.iti.kit.edu/).

## Download
```
git clone https://github.com/carlons/network_scanner.git
```

## Install

```
cd dist/

sudo pip3 install network_scanner-0.1.0-py3-none-any.whl
```

## Usage

### Input format

1. Network data file

    > Only support edgelist format. Each row has two columns which seperated by tab. The first column is source id, and the second column is target id.
    >
    > For example:
    >
    > 1 2
    >
    > 1 33
    >
    > 3 42
    >
    > 45  67
    >  
    > ...

1. Index file:

    > This file records the name of each node in the network. It has two columns which seperated by tab. The first column is node id, and the second column is node name.
    > For example:
    >
    > 1 'hello'
    >
    > 2 'world'
    >
    > 3 'three'
    >
    > 33  'John'
    >  
    > 42 'Ramos'
    >
    > 45 'Ronaldo'
    >
    > 67 'Ozil'
    >
    >...


### Function example
Complete codes are in example.py.

First import necessary moudle.
```
import network_scanner
from network_scanner.networkit_based import degree_analysis
from network_scanner.networkit_based import calculate_betweeness
from network_scanner.networkit_based import centrality_analysis
from network_scanner.networkit_based import networkit_util
from network_scanner.networkit_based import networkit_analysis

```
Then set global parameters.

```
filepath = './input/toy_graph'
label = 'toy'
outpath = './output/' + label + '/'
```

Now we can scan this network.

#### 1. general analysis
  ```
    networkit_analysis.analysis(filepath, label, outpath, directed=False)
    networkit_analysis.analysis(filepath, label, outpath, directed=True)
  ```
#### 2. degree analysis
  - get top k's name
  ```
    false_id_value_filename = outpath + 'toy-falseid-degree'
    map_filename = outpath + 'undirected-toy-map-node-ids'
    index_filename = './input/index'
    result_filename = outpath + label + 'degree-top-k-trueid-value'
    k = 3
    paras = {'false_id_value_filename': false_id_value_filename, 'map_filename': map_filename,
              'index_filename': index_filename, 'result_filename': result_filename, 'k': k
    degree_analysis.get_top_k_trueid_and_name(**paras)
  ```
  - fit powerlaw distribution
  ```
    net = networkit_util.readnetwork(filepath, directed=False)
    degree_analysis.get_deg_seq(net, label, outpath, degree_type='all')
    degree_seq_filename = outpath + 'toy-all-degree'
    degree_analysis.power_law_analysis(degree_seq_filename, label, outpath, degree_type='all')
  ```
  - indegree vs outdegree
  ```
    indeg_falseid_value_filename = outpath + 'toy-falseid-indegree'
    outdeg_falseid_value_filename = outpath + 'toy-falseid-outdegree'
    map_filename = outpath + 'directed-toy-map-node-ids'
    index_filename = './input/index'
    result_filename = outpath + label + 'indeg-vs-outdeg'
    paras = {'indeg_falseid_value_filename': indeg_falseid_value_filename,
             'outdeg_falseid_value_filename': outdeg_falseid_value_filename, 'map_filename': map_filename,
              'index_filename': index_filename, 'result_filename': result_filename}
    degree_analysis.get_top_in_out_degree_cmp(**paras)
  ```
#### 3. distance analysis
    ```
    net = networkit_util.readnetwork(filepath, directed=False)
    lcc_subgraph = networkit_util.get_lcc_subgraph(net)
    logging.info('plot hop...')
    paras = dict(net=lcc_subgraph, label=label, outpath=outpath)
    networkit_plot.plot_hop_dist(**paras)
    logging.info('')
    logging.info('estimate average shortest path')
    sample_num = 100
    logging.info('sample size: {0}'.format(sample_num))
    asp = networkit_util.get_average_shortest_path_appro(lcc_subgraph, sample_num=sample_num)
    logging.info('estimated average shortest path: {0}'.format(asp))
    ```
#### 4. calculate betweeness centrality
  ```
    net = networkit_util.readnetwork(filepath, directed=False)
    calculate_betweeness.get_betweeness(net, label, outpath)
  ```

#### 5. centrality analysis
  ```
    pagerank_filename = outpath + 'toy-pagerank-falseid-value'
    map_filename = outpath + 'directed-toy-map-node-ids'
    top_k_list = centrality_analysis.get_top_k_id(pagerank_filename, map_filename, 3)
    print(top_k_list)
    index_filename = './input/index'
    top_k_name = centrality_analysis.get_top_k_name(top_k_list, index_filename)
    print(top_k_name)
    centrality_analysis.power_law_analysis(pagerank_filename, 'pagerank', label, outpath)
  ```
