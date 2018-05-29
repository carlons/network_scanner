import os
import knowledge_graph.kg_util as kg_util


def get_triples(raw_filename, triple_filename):
    """
    get triple file from raw data
    :param raw_filename:
    :param triple_filename:
    :return:
    """
    raw_file = open(raw_filename, 'r')
    triple_file = open(triple_filename, 'w')
    # the first line is title
    line = raw_file.readline()
    print(line)
    cnt = 0
    triples = []
    while True:
        line = raw_file.readline()
        if not line:
            break
        cnt = cnt + 1
        splited_line = line.strip().split(sep='\t')
        each_triple = splited_line[0] + '\t' + splited_line[1] + '\t' + splited_line[2]
        triples.append(each_triple)
    print('start to write to disk...')
    print(cnt)
    for ele in triples:
        triple_file.write(ele + '\n')
    raw_file.close()
    triple_file.close()


def get_category_instance_triple(triple_filename, category_instance_filename):
    """
    get category instance triple from all tripe file.
    :param triple_filename:
    :param category_instance_filename:
    :return:
    """
    triple_file = open(triple_filename, 'r')
    category_instance_file = open(category_instance_filename, 'w')
    result = []
    while True:
        line = triple_file.readline()
        if not line:
            break
        splited_line = line.split(sep='\t')
        if splited_line[1] == 'generalizations':
            result.append(line)
    for ele in result:
        category_instance_file.write(ele)
    triple_file.close()
    category_instance_file.close()


def get_relation_instance_triple(triple_filename, relation_instance_filename):
    """
    get relation instance triple from all tripe file.
    :param triple_filename:
    :param relation_instance_filename:
    :return:
    """
    triple_file = open(triple_filename, 'r')
    relation_instance_file = open(relation_instance_filename, 'w')
    result = []
    while True:
        line = triple_file.readline()
        if not line:
            break
        splited_line = line.split(sep='\t')
        if splited_line[1] != 'generalizations':
            result.append(line)
    for ele in result:
        relation_instance_file.write(ele)
    triple_file.close()
    relation_instance_file.close()


if __name__ == '__main__':
    raw_filename = '../input/NELL/NELL.08m.1105.esv.csv'
    outpath = 'output/NELL/'
    triple_filename = outpath + 'nell-triple'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # 1. get triple file from raw file
    # paras = {'raw_filename': raw_filename, 'triple_filename': triple_filename}
    # get_triples(**paras)

    # 2. get category instance file from triple file
    # category_instance_filename = outpath + 'nell-triple-category-instance-triple'
    # paras = {'triple_filename': triple_filename, 'category_instance_filename': category_instance_filename}
    # get_category_instance_triple(**paras)

    # 3. get category instance file from triple file
    # relation_instance_filename = outpath + 'nell-triple-relation-instance-triple'
    # paras = {'triple_filename': triple_filename, 'relation_instance_filename': relation_instance_filename}
    # get_relation_instance_triple(**paras)

    # 4. get unique entity, catogory, relation etc.
    # 4.1 get unique relations from triple file. including generalizations.
    # unique_relations = outpath + 'nell-triple-unique-relations'
    # paras = {'filename': triple_filename, 'unique_filename': unique_relations, 'which_col': 'p'}
    # kg_util.get_unique(**paras)
    # 4.2 get unique category from category-instance-triples
    # category_instance_filename = outpath + 'nell-triple-category-instance-triple'
    # unique_category = outpath + 'nell-triple-category-instance-triple-category'
    # paras = {'filename': category_instance_filename, 'unique_filename': unique_category, 'which_col': 'o'}
    # kg_util.get_unique(**paras)
    # 4.3 get unique entity from relation-instance-triples
    # relation_instance_filename = outpath + 'nell-triple-relation-instance-triple'
    # unique_entity = outpath + 'nell-triple-relation-instance-triple-entity'
    # paras = {'filename': relation_instance_filename, 'unique_filename': unique_entity, 'which_col': 'p'}
    # kg_util.get_unique(**paras)

    # 5. get unique category and entity from all triple file
    # index_before = outpath + 'nell-triple-index-before'
    # paras = {'filename': triple_filename, 'unique_filename': index_before, 'which_col': 'so'}
    # kg_util.get_unique(**paras)

    # 6. add index to above unique file
    # index_before = outpath + 'nell-triple-index-before'
    # index_after = outpath + 'nell-triple-index-after'
    # paras = {'unique_filename': index_before, 'index_unique_filename': index_after}
    # kg_util.create_index(**paras)

    # 7. convert triple file to id pair file
    index_after = outpath + 'nell-triple-index-after'
    # 7.1 convert all triple file to id pair file
    # id_pair_filename = outpath + 'nell-all-id-pair'
    # paras = dict(filename=triple_filename, index_filename=index_after, id_pair_filename=id_pair_filename, cols='three')
    # kg_util.raw_to_id_pair(**paras)
    # 7.2 convert category instance file to id pair file
    # category_instance_filename = outpath + 'nell-triple-category-instance-triple'
    # id_pair_filename = outpath + 'nell-category-instance-id-pair'
    # paras = dict(filename=category_instance_filename, index_filename=index_after, id_pair_filename=id_pair_filename, cols='three')
    # kg_util.raw_to_id_pair(**paras)
    # 7.3 convert relation instance triple file to id pair file
    relation_instance_filename = outpath + 'nell-triple-relation-instance-triple'
    id_pair_filename = outpath + 'nell-relation-instance-id-pair'
    paras = dict(filename=relation_instance_filename, index_filename=index_after, id_pair_filename=id_pair_filename, cols='three')
    kg_util.raw_to_id_pair(**paras)