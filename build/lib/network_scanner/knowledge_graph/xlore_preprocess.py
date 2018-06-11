def get_id_pair(triple_filename, source_dest_filename):
    triple_file = open(triple_filename, 'r')
    source_dest_file = open(source_dest_filename, 'w')
    line = triple_file.readline()
    while True:
        line = triple_file.readline()
        if not line:
            break
        split_line = line.strip().split()
        source_dest_file.write(str(split_line[0]) + '\t' + str(split_line[1]) + '\n')
    triple_file.close()
    source_dest_file.close()


if __name__ == '__main__':
    triple_filename = '/home/carlons/openke/freebase/triple2id.txt'
    source_dest_filename = '/home/carlons/openke/freebase/freebase-id-pair.txt'
    get_id_pair(triple_filename, source_dest_filename)