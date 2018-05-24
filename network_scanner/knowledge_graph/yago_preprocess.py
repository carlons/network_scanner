import os
import knowledge_graph.kg_util as kg_util


def get_triple_file(raw_filename, triple_filename):
    """
    get triple file from raw file
    :param raw_filename:
    :param triple_filename:
    :return:
    """
    raw_file = open(raw_filename, 'r')
    triple_file = open(triple_filename, 'w')
    # pass the first line
    line = raw_file.readline()
    while True:
        line = raw_file.readline()
        if not line:
            break
        splited_line = line.strip().split(sep='\t')
        triple = splited_line[1] + '\t' + splited_line[2] + '\t' + splited_line[3] + '\n'
        triple_file.write(triple)
    raw_file.close()
    triple_file.close()


def create_all_index(classes_filename, instance_filename, literal_filename, index_filename):
    """
    create all index.
    :param classes_filename:
    :param instance_filename:
    :param literal_filename:
    :param index_filename:
    :return:
    """
    classes_file = open(classes_filename, 'r')
    instance_file = open(instance_filename, 'r')
    literal_file = open(literal_filename, 'r')
    index_file = open(index_filename, 'w')
    cnt = 1
    while True:
        line = classes_file.readline()
        if not line:
            break
        index_file.write(str(cnt) + '\t' + line.strip() + '\n')
        cnt = cnt + 1
    while True:
        line = literal_file.readline()
        if not line:
            break
        index_file.write(str(cnt) + '\t' + line.strip() + '\n')
        cnt = cnt + 1
    while True:
        line = instance_file.readline()
        if not line:
            break
        index_file.write(str(cnt) + '\t' + line.strip() + '\n')
        cnt = cnt + 1
    classes_file.close()
    instance_file.close()
    literal_file.close()
    index_file.close()


def create_id_pair(**paras):
    """
    convert to id pair
    :param paras:
    :return:
    """
    subclass_relation_filename = paras['subclass_relation_filename']
    instance_type_filename = paras['instance_type_filename']
    facts_filename = paras['facts_filename']
    literal_facts_filename = paras['literal_facts_filename']
    date_facts_filename = paras['date_facts_filename']
    all_index_filename = paras['all_index_filename']
    string_pair_filename = paras['string_pair_filename']
    id_pair_filename = paras['id_pair_filename']
    which = paras['which']
    # get index map
    all_index = dict()
    all_index_file = open(all_index_filename, 'r')
    while True:
        line = all_index_file.readline()
        if not line:
            break
        splitted_line = line.strip().split(sep='\t')
        all_index[splitted_line[1]] = splitted_line[0]
    all_index_file.close()
    string_pair_file = open(string_pair_filename, 'w')
    id_pair_file = open(id_pair_filename, 'w')
    # determine generate which id pair
    if which == 'all':
        subclass_pair = kg_util.get_pair(subclass_relation_filename, sep='\t', cols=[0, 2])
        for ele in subclass_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        instance_type_pair = kg_util.get_pair(instance_type_filename, sep='\t', cols=[0, 2])
        for ele in instance_type_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        facts_filename_pair = kg_util.get_pair(facts_filename, sep='\t', cols=[0, 2])
        for ele in facts_filename_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        literal_facts_filename_pair = kg_util.get_pair(literal_facts_filename, sep='\t', cols=[0, 2])
        for ele in literal_facts_filename_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        date_facts_filename_pair = kg_util.get_pair(date_facts_filename, sep='\t', cols=[0, 2])
        for ele in date_facts_filename_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
    string_pair_file.close()
    id_pair_file.close()


if __name__ == '__main__':
    outpath = './output/YAGO3/all/'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # process yagoFacts file
    # yago_facts_raw_filename = '../input/YAGO3/yagoFacts.tsv'
    # yago_facts_triple_filename = outpath + 'yagoFacts-triple'
    # 1. get triple file from raw file
    # paras = dict(raw_filename=yago_facts_raw_filename, triple_filename=yago_facts_triple_filename)
    # get_triple_file(**paras)

    # 2. get predicate from triple file
    # unique_predicate_filename = outpath + 'yagoFacts-predicate'
    # paras = dict(filename=yago_facts_triple_filename, unique_filename=unique_predicate_filename, which_col='p')
    # kg_util.get_unique(**paras)

    # 3. get instance from triple file
    # unique_instance_filename = outpath + 'yagoFacts-instance'
    # paras = dict(filename=yago_facts_triple_filename, unique_filename=unique_instance_filename, which_col='so')
    # kg_util.get_unique(**paras)

    # ##################################################################################################################

    # process yagoTaxonomy file
    # yago_taxonomy_raw_filename = '../input/YAGO3/yagoTaxonomy.tsv'
    # yago_taxonomy_triple_filename = outpath + 'yagoTaxonomy-triple'
    # # 1. get triple file from raw file
    # paras = dict(raw_filename=yago_taxonomy_raw_filename, triple_filename=yago_taxonomy_triple_filename)
    # get_triple_file(**paras)

    # # 2. get predicate from triple file
    # unique_predicate_filename = outpath + 'yagoTaxonomy-predicate'
    # paras = dict(filename=yago_taxonomy_triple_filename, unique_filename=unique_predicate_filename, which_col='p')
    # kg_util.get_unique(**paras)
    #
    # # 3. get class from triple file
    # unique_class_filename = outpath + 'yagoTaxonomy-class'
    # paras = dict(filename=yago_taxonomy_triple_filename, unique_filename=unique_class_filename, which_col='so')
    # kg_util.get_unique(**paras)

    ####################################################################################################################

    # process yagoType file
    # yago_type_raw_filename = '../input/YAGO3/yagoTypes.tsv'
    # yago_type_triple_filename = outpath + 'yagoTypes-triple'
    # # 1. get triple file from raw file
    # paras = dict(raw_filename=yago_type_raw_filename, triple_filename=yago_type_triple_filename)
    # get_triple_file(**paras)
    #
    # # 2. get predicate from triple file
    # unique_predicate_filename = outpath + 'yagoTypes-predicate'
    # paras = dict(filename=yago_type_triple_filename, unique_filename=unique_predicate_filename, which_col='p')
    # kg_util.get_unique(**paras)
    #
    # # 3. get subject from triple file
    # unique_subject_filename = outpath + 'yagoTypes-subject'
    # paras = dict(filename=yago_type_triple_filename, unique_filename=unique_subject_filename, which_col='s')
    # kg_util.get_unique(**paras)
    #
    # # 4. get object from triple file
    # unique_object_filename = outpath + 'yagoTypes-object'
    # paras = dict(filename=yago_type_triple_filename, unique_filename=unique_object_filename, which_col='o')
    # kg_util.get_unique(**paras)

    ####################################################################################################################

    # combine Taxonomy, Types, Facts
    # 1. difference between class in taxonomy and object in types
    # types_object_filename = outpath + 'yagoTypes-object'
    # taxonomy_class_filename = outpath + 'yagoTaxonomy-class'
    # types_object_differ_taxonomy_class = outpath + 'types-object-differ-taxonomy-class'
    # paras = dict(filename_one=types_object_filename, filename_two=taxonomy_class_filename,
    #              result_filename=types_object_differ_taxonomy_class)
    # kg_util.get_difference(**paras)

    # 2. difference between instance in yagoFacts and subject in yagotypes
    # yago_facts_instance_filename = outpath + 'yagoFacts-instance'
    # yago_types_subject_filename = outpath + 'yagoTypes-subject'
    # facts_instance_differ_types_subject = outpath + 'facts-instance-differ-types-subject'
    # types_subject_differ_facts_instance = outpath + 'types-subject-differ-facts-instance'
    # # paras = dict(filename_one=yago_facts_instance_filename, filename_two=yago_types_subject_filename,
    # #            result_filename=facts_instance_differ_types_subject)
    # paras = dict(filename_one=yago_types_subject_filename, filename_two=yago_facts_instance_filename,
    #              result_filename=types_subject_differ_facts_instance)
    # kg_util.get_difference(**paras)

    # 3. create index file
    # classes_filename = outpath + 'yagoTaxonomy-class'
    # facts_instance_filename = outpath + 'yagoFacts-instance'
    # types_subject_filename = outpath + 'yagoTypes-subject'
    # index_filename = outpath + 'class-instance-index'
    # paras = dict(classes_filename=classes_filename, facts_instance_filename=facts_instance_filename,
    #              types_subject_filename=types_subject_filename, index_filename=index_filename)
    # create_all_index(**paras)

    # 4. create id pair
    # subclass_relation_filename = outpath + 'yagoTaxonomy-triple'
    # instance_type_filename = outpath + 'yagoTypes-triple'
    # raw_filename = outpath + 'yagoFacts-triple'
    # all_index_filename = outpath + 'class-instance-index'
    # # 4.1 cerate all id pair
    # string_pair_filename = outpath + 'all-string-pair'
    # id_pair_filename = outpath + 'taxonomy-types-facts-id-pair'
    # which = 'all'
    # paras = dict(subclass_relation_filename=subclass_relation_filename, instance_type_filename=instance_type_filename,
    #              raw_filename=raw_filename, all_index_filename=all_index_filename,
    #              string_pair_filename=string_pair_filename, id_pair_filename=id_pair_filename, which=which)
    # create_id_pair(**paras)
    # # 4.2 cerate facts id pair
    # string_pair_filename = outpath + 'facts-string-pair'
    # id_pair_filename = outpath + 'facts-id-pair'
    # which = 'facts'
    # paras = dict(subclass_relation_filename=subclass_relation_filename, instance_type_filename=instance_type_filename,
    #              raw_filename=raw_filename, all_index_filename=all_index_filename,
    #              string_pair_filename=string_pair_filename, id_pair_filename=id_pair_filename, which=which)
    # create_id_pair(**paras)

    #################################################################################################
    # # ADD literal facts
    # yago_literal_facts_raw_filename = '../input/YAGO3/yagoLiteralFacts.tsv'
    # yago_literal_facts_triple_filename = outpath + 'yagoLiteralFacts-triple'
    # # 1. get triple file from raw file
    # # paras = dict(raw_filename=yago_literal_facts_raw_filename, triple_filename=yago_literal_facts_triple_filename)
    # # get_triple_file(**paras)
    # # filename = yago_literal_facts_triple_filename
    # # unique_filename = outpath + 'yago-literal-predicate'
    # # paras = dict(filename=filename, unique_filename=unique_filename, which_col='p', sep='\t')
    # # kg_util.get_unique(**paras)
    # filename = yago_literal_facts_triple_filename
    # unique_filename = outpath + 'yago-literal-subject'
    # paras = dict(filename=filename, unique_filename=unique_filename, which_col='s', sep='\t')
    # kg_util.get_unique(**paras)
    # filename = yago_literal_facts_triple_filename
    # unique_filename = outpath + 'yago-literal-object'
    # paras = dict(filename=filename, unique_filename=unique_filename, which_col='o', sep='\t')
    # kg_util.get_unique(**paras)

    # ADD date facts
    # yago_date_facts_raw_filename = '../input/YAGO3/yagoDateFacts.tsv'
    # yago_date_facts_triple_filename = outpath + 'yagoDateFacts-triple'
    # # 1. get triple file from raw file
    # # paras = dict(raw_filename=yago_date_facts_raw_filename, triple_filename=yago_date_facts_triple_filename)
    # # get_triple_file(**paras)
    # # filename = yago_date_facts_triple_filename
    # # unique_filename = outpath + 'yago-date-predicate'
    # # paras = dict(filename=filename, unique_filename=unique_filename, which_col='p', sep='\t')
    # # kg_util.get_unique(**paras)
    # filename = yago_date_facts_triple_filename
    # unique_filename = outpath + 'yago-date-subject'
    # paras = dict(filename=filename, unique_filename=unique_filename, which_col='s', sep='\t')
    # kg_util.get_unique(**paras)
    # filename = yago_date_facts_triple_filename
    # unique_filename = outpath + 'yago-date-object'
    # paras = dict(filename=filename, unique_filename=unique_filename, which_col='o', sep='\t')
    # kg_util.get_unique(**paras)

    # 3. create index file
    # classes_filename = outpath + 'yagoTaxonomy-class'
    #
    # facts_instance_filename = outpath + 'yagoFacts-instance'
    # types_subject_filename = outpath + 'yagoTypes-subject'
    # literal_facts_subject_filename = outpath + 'yago-literal-subject'
    # data_facts_subject_filename = outpath + 'yago-date-subject'
    #
    # literal_facts_object_filename = outpath + 'yago-literal-object'
    # data_facts_object_filename = outpath + 'yago-date-object'
    #
    # all_instance_filename = outpath + 'yago-all-instance'
    # all_literal_filename = outpath + 'yago-all-literal'
    # index_filename = outpath + 'yago-all-index'
    #
    # kg_util.merge_two_file(facts_instance_filename, types_subject_filename, all_instance_filename)
    # kg_util.merge_two_file(all_instance_filename, literal_facts_subject_filename, all_instance_filename)
    # kg_util.merge_two_file(all_instance_filename, data_facts_subject_filename, all_instance_filename)
    #
    # kg_util.merge_two_file(literal_facts_object_filename, data_facts_object_filename, all_literal_filename)
    #
    # paras = dict(classes_filename=classes_filename, instance_filename=all_instance_filename,
    #              literal_filename=all_literal_filename, index_filename=index_filename)
    # create_all_index(**paras)

    # 4. create id pair
    subclass_relation_filename = outpath + 'yagoTaxonomy-triple'
    instance_type_filename = outpath + 'yagoTypes-triple'
    facts_filename = outpath + 'yagoFacts-triple'
    literal_facts_filename = outpath + 'yagoLiteralFacts-triple'
    date_facts_filename = outpath + 'yagoDateFacts-triple'
    all_index_filename = outpath + 'yago-all-index'
    # 4.1 cerate all id pair
    string_pair_filename = outpath + 'all-string-pair'
    id_pair_filename = outpath + 'taxonomy-types-facts-literal-date-id-pair'
    which = 'all'
    paras = dict(subclass_relation_filename=subclass_relation_filename, instance_type_filename=instance_type_filename,
                 facts_filename=facts_filename, literal_facts_filename=literal_facts_filename,
                 date_facts_filename=date_facts_filename, all_index_filename=all_index_filename,
                 string_pair_filename=string_pair_filename, id_pair_filename=id_pair_filename, which=which)
    create_id_pair(**paras)