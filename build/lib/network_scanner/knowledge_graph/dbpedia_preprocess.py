# coding: utf-8
import os
import ontospy
import knowledge_graph.kg_util as kg_util


def analysis_ontology(ontology_filename, outpath):
    """
    get general information about ontology file
    :param ontolofy_filename:
    :param outpath:
    :return:
    """
    onto = ontospy.Ontospy(ontology_filename)

    stas = onto.stats()
    onto_info = open(outpath + 'info', 'w')
    for ele in stas:
        for item in ele:
            onto_info.write(str(item) + ' ')
        onto_info.write('\n')
    onto_info.close()

    classes = onto.classes
    classes_file = open(outpath + 'classes', 'w')
    for ele in classes:
        ele = str(ele)
        ele_start = ele.index('*')
        ele_end = ele.rindex('*')
        ele = '<' + ele[ele_start + 1:ele_end] + '>'
        classes_file.write(ele + '\n')
    classes_file.close()

    data_property = onto.datatypeProperties
    data_property_file = open(outpath + 'data_property', 'w')
    for ele in data_property:
        data_property_file.write(str(ele) + '\n')
    data_property_file.close()

    object_property = onto.objectProperties
    object_property_file = open(outpath + 'object_property', 'w')
    for ele in object_property:
        object_property_file.write(str(ele) + '\n')
    object_property_file.close()


def get_subclass_relation(ontology_filename, subclass_relation_filename):
    """
    get subclass relation pair
    :param ontology_filename:
    :param subclass_relation_filename:
    :return:
    """
    onto = ontospy.Ontospy(ontology_filename, 'r')
    classes = onto.classes
    result = []
    for c in classes:
        c_parents = c.parents()
        if c_parents is not None:
            for p in c_parents:
                result.append((c, p))
    subclass_relation_file = open(subclass_relation_filename, 'w')
    for ele in result:
        # ontospy has its own class format. Here we extract class
        child = str(ele[0])
        parent = str(ele[1])
        child_start = child.index('*')
        child_end = child.rindex('*')
        parent_start = parent.index('*')
        parent_end = parent.rindex('*')
        child = '<' + child[child_start+1:child_end] + '>'
        parent = '<' + parent[parent_start+1:parent_end] + '>'
        subclass_relation_file.write(child + '\t' + parent + '\n')
    subclass_relation_file.close()


def extract(instance_type_filename, mappingbased_instance_filename, extracted_instance_types_filename):
    """
    从Instance Types中抽取subject也出现在Mappingbased Objects的那些行
    :param instance_type_filename:
    :param mappingbased_instance_filename:
    :param extracted_instance_types_filename:
    :return:
    """
    instance_type_file = open(instance_type_filename, 'r')
    mappingbased_instance_file = open(mappingbased_instance_filename, 'r')
    extracted_instance_types_file = open(extracted_instance_types_filename, 'w')
    mappingbased_instance = set()
    while True:
        line = mappingbased_instance_file.readline().strip()
        if not line:
            break
        mappingbased_instance.add(line)
    while True:
        line = instance_type_file.readline()
        if not line:
            break
        splited_line = line.strip().split(sep=' ')
        if splited_line[0] in mappingbased_instance:
            extracted_instance_types_file.write(line)
    instance_type_file.close()
    mappingbased_instance_file.close()
    extracted_instance_types_file.close()


def create_all_index(classes_filename, instance_filename, literal_object_filename, index_filename):
    """
    create all index.
    :param classes_filename:
    :param instance_filename:
    :param literal_object_filename:
    :param index_filename:
    :return:
    """
    classes_file = open(classes_filename, 'r')
    instance_file = open(instance_filename, 'r')
    literal_file = open(literal_object_filename, 'r')
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
    mappingbased_object_filename = paras['mappingbased_object_filename']
    mappingbased_literal_filename = paras['mappingbased_literal_filename']
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
        subclass_pair = kg_util.get_pair(subclass_relation_filename, sep='\t', cols=[0, 1])
        for ele in subclass_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[0]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        instance_type_pair = kg_util.get_pair(instance_type_filename, sep=' ', cols=[0, 2])
        for ele in instance_type_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        mappingbased_object_filename_pair = kg_util.get_pair(mappingbased_object_filename, sep=' ', cols=[0, 2])
        for ele in mappingbased_object_filename_pair:
            source_id = all_index.get(str(ele[0]))
            target_id = all_index.get(str(ele[1]))
            if not source_id or not target_id:
                print(ele[0], ele[1])
                continue
            string_pair_file.write(str(ele[0]) + '\t' + str(ele[1]) + '\n')
            id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
        mappingbased_literal_filename_pair = kg_util.get_pair(mappingbased_literal_filename, sep=' ', cols=[0, 2])
        for ele in mappingbased_literal_filename_pair:
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
    outpath = 'output/DBpedia/all/'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # Process Ontology file
    # ontology_filename = '../input/DBpedia/dbpedia_2016-10.owl'
    # 1. analysis ontology file.
    # paras = dict(ontology_filename=ontology_filename, outpath=outpath)
    # analysis_ontology(**paras)

    # 2. get subclass of relations
    # subclass_relation_filename = outpath + 'subclass-pair'
    # paras = dict(ontology_filename=ontology_filename, subclass_relation_filename=subclass_relation_filename)
    # get_subclass_relation(**paras)

    # 3. how many unique classes in subclass of relations
    # subclass_relation_filename = outpath + 'subclass-pair'
    # subclass_relation_unique_class = outpath + 'subclass-unique-class'
    # paras = dict(filename=subclass_relation_filename, unique_filename=subclass_relation_unique_class, which_col='sp')
    # kg_util.get_unique(**paras)

    ###################################################################################################################

    # Process Mappingbased Objects
    # delete 1st and last line in raw file, they are comments.
    # raw_filename = '../input/DBpedia/mappingbased_objects_en.ttl'
    # 1. get all properties in raw file
    # object_property_filenme = outpath + 'mappingbased-object-property'
    # paras = dict(filename=raw_filename, unique_filename=object_property_filenme, which_col='p')
    # kg_util.get_unique(**paras)

    # 2. get unique instance in mappingbased file
    # instance_filename = outpath + 'mappingbased-unique-instance'
    # paras = dict(filename=raw_filename, unique_filename=instance_filename, which_col='so')
    # kg_util.get_unique(**paras)

    # 3. create index
    # instance_filename = outpath + 'mappingbased-unique-instance'
    # index_filename = outpath + 'mappingbased-instance-index'
    # paras = dict(unique_filename=instance_filename, index_unique_filename=index_filename)
    # kg_util.create_index(**paras)

    # 4. convert raw to id pair
    # index_filename = outpath + 'mappingbased-instance-index'
    # id_pair_filename = outpath + 'mappingbased-id-pair'
    # paras = dict(filename=raw_filename, index_filename=index_filename, id_pair_filename=id_pair_filename, cols='three')
    # kg_util.raw_to_id_pair(**paras)

    ##################################################################################################################

    # Process Instance Types
    # delete 1st and last line in raw file, they are comments.
    # raw_filename = '../input/DBpedia/instance_types_en.ttl'
    # 1. get all predicates from instance-types file
    # predicate_filename = outpath + 'instance-types-predicate'
    # paras = dict(filename=raw_filename, unique_filename=predicate_filename, which_col='p')
    # kg_util.get_unique(**paras)

    # 2. get all subjects from instace-types file
    # subject_filename = outpath + 'instance-types-subject'
    # paras = dict(filename=raw_filename, unique_filename=subject_filename, which_col='s')
    # kg_util.get_unique(**paras)

    # 3. get all objects from instace-types file
    # object_filename = outpath + 'instance-types-object'
    # paras = dict(filename=raw_filename, unique_filename=object_filename, which_col='o')
    # kg_util.get_unique(**paras)

    ##################################################################################################################

    # combine Ontology, Mappingbased Objects and Instance Types
    # 1. extract instance types
    # instance_type_filename = '../input/DBpedia/instance_types_en.ttl'
    # mappingbased_instance_filename = outpath + 'mappingbased-unique-instance'
    # extracted_instance_types_filename = outpath + 'extracted_instance_types'
    # paras = dict(instance_type_filename=instance_type_filename,
    #               mappingbased_instance_filename=mappingbased_instance_filename,
    #               extracted_instance_types_filename=extracted_instance_types_filename)
    # extract(**paras)

    # 2. difference between class in instancetype and class in ontology
    # ontology_class_filename = outpath + 'classes'
    # instance_object_filename = outpath + 'instance-types-object'
    # difference_file = outpath + 'ontology_class_differ_instance_type'
    # paras = dict(filename_one=ontology_class_filename, filename_two=instance_object_filename, result_filename=difference_file)
    # kg_util.get_difference(**paras)

    # 3. difference between class in instancetype and class in sunClassOf relation
    # subclass_unique_class_filename = outpath + 'subclass-unique-class'
    # instance_object_filename = outpath + 'instance-types-object'
    # difference_file = outpath + 'subclass_differ_instance_type'
    # paras = dict(filename_one=subclass_unique_class_filename, filename_two=instance_object_filename,
    #              result_filename=difference_file)
    # kg_util.get_difference(**paras)

    # 4. difference between class in ontology and instance in mappingbased object
    # ontology_class_filename = outpath + 'classes'
    # mappingbased_instance_filename = outpath + 'mappingbased-unique-instance'
    # difference_file = outpath + 'ontology_class_differ_mappingbased_instance'
    # paras = dict(filename_one=ontology_class_filename, filename_two=mappingbased_instance_filename, result_filename=difference_file)
    # kg_util.get_difference(**paras)

    # 5. create all index. including class and instance in mappingbased object
    # ontology_class_filename = outpath + 'classes'
    # instance_filename = outpath + 'mappingbased-unique-instance'
    # index_filename = outpath + 'ontology-mappingbased-index'
    # paras = dict(classes_filename=ontology_class_filename, instance_filename=instance_filename, index_filename=index_filename)
    # create_all_index(**paras)

    # 6. combine ontology, instancetype and mappingbased to one single id pair file
    # subclass_relation_filename = outpath + 'subclass-pair'
    # instance_type_filename = '../input/DBpedia/instance_types_en.ttl'
    # raw_filename = '../input/DBpedia/mappingbased_objects_en.ttl'
    # all_index_filename = outpath + 'ontology-mappingbased-index'
    # 6.1 create all id pair
    # all_string_pair_filename = outpath + 'ontology_instancetype_mappingbased_string_pair'
    # all_id_pair_filename = outpath + 'ontology_instancetype_mappingbased_id_pair'
    # which = 'all'
    # paras = dict(subclass_relation_filename=subclass_relation_filename, instance_type_filename=instance_type_filename,
    #              raw_filename=raw_filename, all_index_filename=all_index_filename,
    #              string_pair_filename=all_string_pair_filename,
    #              id_pair_filename=all_id_pair_filename, which=which)
    # 6.2 create mappingbased id pair
    # instance_string_pair_filename = outpath + 'mappingbased_string_pair'
    # instance_id_pair_filename = outpath + 'mappingbased_id_pair'
    # which = 'instance'
    # paras = dict(subclass_relation_filename=subclass_relation_filename, instance_type_filename=instance_type_filename,
    #              raw_filename=raw_filename, all_index_filename=all_index_filename,
    #              string_pair_filename=instance_string_pair_filename,
    #              id_pair_filename=instance_id_pair_filename, which=which)
    # create_id_pair(**paras)

    ################################################################################################################

    # # ADD Literal Facts
    # # 1. analysis literal
    # # 1.1 get unique predicate
    # literal_filename = '../input/DBpedia/mappingbased_literals_en.ttl'
    # unique_relation_filename = outpath + 'literal-predicate'
    # paras = dict(filename=literal_filename, unique_filename=unique_relation_filename, which_col='p', sep=' ')
    # kg_util.get_unique(**paras)
    # # 1.2 get unique subject
    # literal_filename = '../input/DBpedia/mappingbased_literals_en.ttl'
    # unique_relation_filename = outpath + 'literal-subject'
    # paras = dict(filename=literal_filename, unique_filename=unique_relation_filename, which_col='s', sep=' ')
    # kg_util.get_unique(**paras)
    # # 1.3 get unique object
    # literal_filename = '../input/DBpedia/mappingbased_literals_en.ttl'
    # unique_relation_filename = outpath + 'literal-object'
    # paras = dict(filename=literal_filename, unique_filename=unique_relation_filename, which_col='o', sep=' ')
    # kg_util.get_unique(**paras)

    #######################################################################################################

    # CREATE GRAPG INCLUDE ALL: ontology, instance-type, mappingbased-object, mappingbased-literal
    # 1. get subject and object
    # subclass_relation_filename = outpath + 'subclass-pair'
    # ontology_class_filename = outpath + 'classes'
    # kg_util.get_unique(subclass_relation_filename, ontology_class_filename, which_col='sp')
    #
    # instance_type_filename = '../input/DBpedia/instance_types_en.ttl'
    # instance_types_subject_filename = outpath + 'instance-types-subject'
    # instance_types_object_filename = outpath + 'instance-types-object'
    # kg_util.get_unique(instance_type_filename, instance_types_subject_filename, which_col='s', sep=' ')
    # kg_util.get_unique(instance_type_filename, instance_types_object_filename, which_col='o', sep=' ')
    #
    # mappingbased_object_filename = '../input/DBpedia/mappingbased_objects_en.ttl'
    # mappingbased_instance_filename = outpath + 'mappingbased-unique-instance'
    # kg_util.get_unique(mappingbased_object_filename, mappingbased_instance_filename, which_col='so', sep=' ')
    #
    # mappingbased_literal_filename = '../input/DBpedia/mappingbased_literals_en.ttl'
    # literal_subject_filename = outpath + 'literal-subject'
    # literal_object_filename = outpath + 'literal-object'
    # kg_util.get_unique(mappingbased_literal_filename, literal_subject_filename, which_col='s', sep=' ')
    # kg_util.get_unique(mappingbased_literal_filename, literal_object_filename, which_col='o', sep=' ')


    # 1. create all index
    # ontology_class_filename = outpath + 'ontology-classes'
    # instance_types_object_filename = outpath + 'instance-types-object'
    #
    # instance_types_subject_filename = outpath + 'instance-types-subject'
    # mappingbased_instance_filename = outpath + 'mappingbased-unique-instance'
    # literal_subject_filename = outpath + 'literal-subject'
    #
    # literal_object_filename = outpath + 'literal-object'
    #
    # all_class_filanme = outpath + 'all_class'
    # all_instance_filename = outpath + 'all_unique_instance'
    #
    # kg_util.merge_two_file(ontology_class_filename, instance_types_object_filename, all_class_filanme)
    # kg_util.merge_three_file(instance_types_subject_filename, mappingbased_instance_filename,
    #                          literal_subject_filename, all_instance_filename)
    # index_filename = outpath + 'all-index'
    # paras = dict(classes_filename=all_class_filanme, instance_filename=all_instance_filename,
    #              literal_object_filename=literal_object_filename, index_filename=index_filename)
    # create_all_index(**paras)

    # 2. combine ontology, instancetype and mappingbased-object, mappingbased-literal to one single id pair file
    subclass_relation_filename = outpath + 'subclass-pair'
    instance_type_filename = '../input/DBpedia/instance_types_en.ttl'
    mappingbased_literal_filename = '../input/DBpedia/mappingbased_literals_en.ttl'
    mappingbased_object_filename = '../input/DBpedia/mappingbased_objects_en.ttl'
    all_index_filename = outpath + 'all-index'
    # 6.1 create all id pair
    all_string_pair_filename = outpath + 'all_string_pair'
    all_id_pair_filename = outpath + 'all_id_pair'
    which = 'all'
    paras = dict(subclass_relation_filename=subclass_relation_filename,
                 instance_type_filename=instance_type_filename,
                 mappingbased_object_filename=mappingbased_object_filename,
                 mappingbased_literal_filename=mappingbased_literal_filename,
                 all_index_filename=all_index_filename,
                 string_pair_filename=all_string_pair_filename,
                 id_pair_filename=all_id_pair_filename, which=which)
    create_id_pair(**paras)