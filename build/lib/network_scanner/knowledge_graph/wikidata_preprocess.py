import os
from network_scanner.knowledge_graph import kg_util


def process():
    outpath = '/home/carlons/wikidata_rdf/output/'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # # statements subject and object
    # statements_filename = '/home/carlons/wikidata_rdf/wikidata-simple-statements.nt'
    # unique_filename = outpath + 'wikidata-simple-statements-subject-object'
    # kg_util.get_unique(statements_filename, unique_filename, which_col='so', sep=' ')

    # # instances subject and object
    # instances_filename = '/home/carlons/wikidata_rdf/wikidata-instances.nt'
    # unique_filename = outpath + 'wikidata-instances-subject-object'
    # kg_util.get_unique(instances_filename, unique_filename, which_col='so', sep=' ')

    # # taxonomy subject and object
    # taxonomy_filename = '/home/carlons/wikidata_rdf/wikidata-taxonomy.nt'
    # unique_filename =  outpath + 'wikidata-taxonomy-subject-object'
    # kg_util.get_unique(taxonomy_filename, unique_filename, which_col='so', sep=' ')

    # # all subject and object
    # statements_unique_filename = outpath + 'wikidata-simple-statements-subject-object'
    # instances_unique_filename = outpath + 'wikidata-instances-subject-object'
    # taxonomy_unique_filename = outpath + 'wikidata-taxonomy-subject-object'
    # all_unique_filename = outpath + 'all-subject-object'
    # kg_util.merge_three_file(statements_unique_filename, instances_unique_filename, taxonomy_unique_filename, all_unique_filename)

    # # create index
    # all_unique_filename = outpath + 'all-subject-object'
    # all_index_filename = outpath + 'all_index'
    # kg_util.create_index(all_unique_filename, all_index_filename)

    # create id pair
    all_index_filename = outpath + 'all_index'
    all_id_pair_filename = outpath + 'wikidata-rdf-id-pair'
    # statements_filename = '/home/carlons/wikidata_rdf/wikidata-simple-statements.nt'
    # kg_util.raw_to_id_pair(statements_filename, all_index_filename, all_id_pair_filename, cols='three')
    # instances_filename = '/home/carlons/wikidata_rdf/wikidata-instances.nt'
    # kg_util.raw_to_id_pair(instances_filename, all_index_filename, all_id_pair_filename, cols='three')
    taxonomy_filename = '/home/carlons/wikidata_rdf/wikidata-taxonomy.nt'
    kg_util.raw_to_id_pair(taxonomy_filename, all_index_filename, all_id_pair_filename, cols='three')


if __name__ == '__main__':
    process()