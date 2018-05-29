import os
import knowledge_graph.kg_util as kg_util


def get_instance_concept_pair(raw_filename, instance_concept_filename):
    """
    get instance_concept file from raw data
    :param raw_filename:
    :param instance_concept_filename:
    :return:
    """
    raw_file = open(raw_filename, 'r')
    instance_concept_file = open(instance_concept_filename, 'w')
    cnt = 0
    result = []
    while True:
        line = raw_file.readline()
        if not line:
            break
        cnt = cnt + 1
        splited_line = line.strip().split(sep='\t')
        each_triple = splited_line[0] + '\t' + splited_line[1]
        result.append(each_triple)
    print('start to write to disk...')
    print(cnt)
    for ele in result:
        instance_concept_file.write(ele + '\n')
    raw_file.close()
    instance_concept_file.close()


if __name__ == '__main__':
    raw_filename = '../input/Probase/data-concept/data-concept-instance-relations.txt'
    outpath = 'output/Probase/'
    instance_concept_filename = outpath + 'probase-instance-concept'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # 1. get instance-concept file from raw data
    # paras = dict(raw_filename=raw_filename, instance_concept_filename=instance_concept_filename)
    # get_instance_concept_pair(**paras)

    # 2. get unique instance from instance-concept file
    # unique_instance_filename = outpath + 'probase-unique-instance'
    # paras = dict(filename=instance_concept_filename, unique_filename=unique_instance_filename, which_col='p')
    # kg_util.get_unique(**paras)

    # 3. get unique concept from instance-concept file
    # unique_concept_filename = outpath + 'probase-unique-concept'
    # paras = dict(filename=instance_concept_filename, unique_filename=unique_concept_filename, which_col='s')
    # kg_util.get_unique(**paras)

    # 4. get unique concept and instance from instance-concept file
    # unique_filename = outpath + 'probase-unique-all'
    # paras = dict(filename=instance_concept_filename, unique_filename=unique_filename, which_col='sp')
    # kg_util.get_unique(**paras)

    # 5. create index
    # unique_filename = outpath + 'probase-unique-all'
    # index_unique_filename = outpath + 'probase-index'
    # paras = dict(unique_filename=unique_filename, index_unique_filename=index_unique_filename)
    # kg_util.create_index(**paras)

    # 6. convert instance-concept to id pair
    index_unique_filename = outpath + 'probase-index'
    id_pair_filename = outpath + 'probase-id-pair'
    paras = dict(filename=instance_concept_filename, index_filename=index_unique_filename, id_pair_filename=id_pair_filename, cols='two')
    kg_util.raw_to_id_pair(**paras)