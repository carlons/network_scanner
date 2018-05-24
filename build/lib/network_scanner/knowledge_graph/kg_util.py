import hashlib
# coding: utf-8


def rm_prefix_predicate(prefix, triple_filename, out_filename):
    """
    delete common prefix to load all data into memory. only process subject and object.
    :param prefix:
    :param triple_filename:
    :param out_filename: two columns
    :return:
    """
    triple_file = open(triple_filename, 'r')
    out_file = open(out_filename, 'w')
    cnt = 0
    while True:
        line = triple_file.readline().strip()
        if not line:
            break
        cnt = cnt + 1
        if cnt % 10000000 == 0:
            print(cnt)
        elements = line.split(sep='\t')
        if len(elements) > 2:
            source = elements[0]
            target = elements[2]
            if source.startswith(prefix):
                source = elements[0][len(prefix):]
            if target.startswith(prefix):
                target = elements[2][len(prefix):]
            out_file.write(str(source) + '\t' + str(target) + '\n')
    triple_file.close()
    out_file.close()


def get_unique(filename, unique_filename, which_col='so', sep='\t'):
    """
    get unique items from triple file.
    :param filename:
    :param unique_filename:
    :param which_col: 's', 'p', 'o', 'so'
    :param sep:
    :return:
    """
    col_orders = {'s': [0], 'p': [1], 'o': [2], 'so': [0, 2], 'sp': [0, 1]}
    col_names = {'s': 'subject', 'p': 'predicate', 'o': 'object', 'so': 'subject-object', 'sp': 'subject-predicate'}

    f = open(filename, 'r')
    out = open(unique_filename + col_names[which_col], 'w')
    unique_elem = set()
    while True:
        line = f.readline()
        if not line:
            break
        elements = line.strip().split(sep=sep)
        for c in col_orders[which_col]:
            unique_elem.add(elements[c])
    for ele in unique_elem:
        out.write(str(ele) + '\n')
    f.close()
    out.close()
    return unique_elem


def create_index(unique_filename, index_unique_filename):
    """
    为unique文件加上index
    :param unique_filename:
    :param index_unique_filename:
    :return:
    """
    f = open(unique_filename, 'r')
    out = open(index_unique_filename, 'w')
    cnt = 1
    while True:
        line = f.readline()
        if not line:
            break
        out.write(str(cnt))
        out.write('\t')
        out.write(str(line))
        cnt = cnt + 1
    f.close()
    out.close()


def raw_to_id_pair(filename, index_filename, id_pair_filename, cols='two'):
    """
    map string pair to id pair.
    :param filename:
    :param index_filename:
    :param id_pair_filename:
    :param cols: indicate the column position of subject and object
    :return:
    """
    col_to_map = {'two': [0, 1], 'three': [0, 2]}
    file = open(filename, 'r')
    index_file = open(index_filename, 'r')
    id_pair_file = open(id_pair_filename, 'w')
    # get string id map
    string_id_map = dict()
    while True:
        line = index_file.readline().strip()
        if not line:
            break
        tmp = line.split(sep='\t')
        string_id_map[tmp[1]] = tmp[0]
    while True:
        line = file.readline().strip()
        if not line:
            break
        elements = line.split(sep=' ')
        source_id = string_id_map.get(elements[col_to_map[cols][0]])
        target_id = string_id_map.get(elements[col_to_map[cols][1]])
        id_pair_file.write(str(source_id) + '\t' + str(target_id) + '\n')
    file.close()
    index_file.close()
    id_pair_file.close()


def hash_unique_file(unique_filename, num, maxsize):
    """
    将unique文件利用hash进行拆分
    :param unique_filename: file path
    :param num: partition number
    :param maxsize: maxsize of dict
    :return: None
    """
    unique_file = open(unique_filename, 'r')
    cnt = 0
    item_map = dict()
    while True:
        line = unique_file.readline().strip()
        if not line:
            break
        cnt = cnt + 1
        # print(line)
        item_hash_value = hashlib.md5(line.encode('utf8')).hexdigest()
        item_hash_index = int(item_hash_value, 16) % num
        if item_hash_index not in item_map:
            item_map[item_hash_index] = [line]
        else:
            item_map.get(item_hash_index).append(line)
        if cnt % maxsize == 0:
            # write to disk and clear dict
            print('write...' + str(cnt))
            for i in range(0, num):
                items = item_map.get(i)
                if not items:
                    continue
                out = open(unique_filename + '_hash_' + str(i), 'a')
                for item in items:
                    out.write(item + '\n')
                out.close()
            item_map.clear()
    # write the rest to disk
    for i in range(0, num):
        items = item_map.get(i)
        if not items:
            continue
        out = open(unique_filename + '_hash_' + str(i), 'a')
        for item in items:
            out.write(item + '\n')
        out.close()
    item_map.clear()
    unique_file.close()


def hash_two_column_file(filename, col, hash_base_filename, num, maxsize):
    """
    将具有两列的文件依据某一列利用hash进行拆分
    :param filename:
    :param col:
    :param hash_base_filename:
    :param num:
    :param maxsize:
    :return:
    """
    unique_file = open(filename, 'r')
    cnt = 0
    item_map = dict()
    while True:
        line = unique_file.readline().strip()
        if not line:
            break
        cnt = cnt + 1
        splited_line = line.split(sep='\t')
        item_hash_value = hashlib.md5(splited_line[col].encode('utf8')).hexdigest()
        item_hash_index = int(item_hash_value, 16) % num
        if item_hash_index not in item_map:
            item_map[item_hash_index] = [line]
        else:
            item_map.get(item_hash_index).append(line)
        if cnt % maxsize == 0:
            # write to disk and clear dict
            print('write...' + str(cnt))
            for i in range(0, num):
                items = item_map.get(i)
                if not items:
                    continue
                out = open(hash_base_filename + str(i), 'a')
                for item in items:
                    out.write(item + '\n')
                out.close()
            item_map.clear()
    # write the rest to disk
    for i in range(0, num):
        items = item_map.get(i)
        if not items:
            continue
        out = open(hash_base_filename + str(i), 'a')
        for item in items:
            out.write(item + '\n')
        out.close()
    item_map.clear()
    unique_file.close()


def string_to_id(string_filename, index_filename, id_filename, col):
    """
    将其中一列的字符串转换为索引数字
    :param string_filename:
    :param index_filename:
    :param id_filename:
    :param col:
    :return:
    """
    string_file = open(string_filename, 'r')
    index_file = open(index_filename, 'r')
    # read index to dict
    index_map = dict()
    while True:
        line = index_file.readline()
        if not line:
            break
        line = line.strip().split(sep='\t')
        index_map[line[1]] = line[0]
    id_file = open(id_filename, 'w')
    while True:
        line = string_file.readline()
        if not line:
            break
        line = line.strip().split(sep='\t')
        line[col] = index_map.get(line[col])
        id_file.write(line[0])
        id_file.write('\t')
        id_file.write(line[1])
        id_file.write('\n')
    id_file.close()
    index_file.close()
    string_file.close()


def string_pair_to_id_pair(string_base_filename, index_base_filename, id_base_filename, num, maxsize):
    # Firstly process source
    col = 0
    for i in range(0, num):
        string_filename = string_base_filename + str(i)
        index_filename = index_base_filename + str(i)
        id_filename = id_base_filename + str(i)
        string_to_id(string_filename, index_filename, id_filename, col)
    # Secondly process target
    col = 1
    # hash based on target
    for i in range(0, num):
        filename = id_base_filename + str(i)
        hash_base_filename = string_base_filename + '-target-' + str(i)
        maxsize = maxsize
        hash_two_column_file(filename=filename, col=col, hash_base_filename=hash_base_filename,
                             num=num, maxsize=maxsize)
    # replace target with id
    for i in range(0, num):
        string_filename = string_base_filename + '-target-' + str(i)
        index_filename = index_base_filename + str(i)
        id_filename = id_base_filename + str(i)
        string_to_id(string_filename, index_filename, id_filename, col)


def get_difference(filename_one, filename_two, result_filename):
    """
    difference between sets
    :param filename_one:
    :param filename_two:
    :param result_filename:
    :return:
    """
    file_one = open(filename_one, 'r')
    file_two = open(filename_two, 'r')
    result = open(result_filename, 'w')
    set_one = set()
    set_two = set()
    while True:
        line = file_one.readline()
        if not line:
            break
        set_one.add(line.strip())
    while True:
        line = file_two.readline()
        if not line:
            break
        set_two.add(line.strip())
    result_set = set_one.difference(set_two)
    for ele in result_set:
        result.write(str(ele) + '\n')
    file_one.close()
    file_two.close()
    result.close()


def get_pair(filename, sep, cols):
    file = open(filename, 'r')
    result = []
    while True:
        line = file.readline()
        if not line:
            break
        splited_line = line.strip().split(sep=sep)
        result.append((splited_line[cols[0]], splited_line[cols[1]]))
    return result


def merge_two_file(filename_one, filename_two, filename_out):
    """
    merge two file
    :param filename_one:
    :param filename_two:
    :param filename_out:
    :return:
    """
    file_one = open(filename_one, 'r')
    result = set()
    while True:
        line = file_one.readline()
        if not line:
            break
        result.add(line.strip())
    file_one.close()

    file_two = open(filename_two, 'r')
    while True:
        line = file_two.readline()
        if not line:
            break
        result.add(line.strip())
    file_two.close()

    file_out = open(filename_out, 'w')
    for item in result:
        file_out.write(str(item) + '\n')
    file_out.close()


def merge_three_file(filename_one, filename_two, filename_three, filename_out):
    """
    merge three file
    :param filename_one:
    :param filename_two:
    :param filename_out:
    :return:
    """
    file_one = open(filename_one, 'r')
    result = set()
    while True:
        line = file_one.readline()
        if not line:
            break
        result.add(line.strip())
    file_one.close()

    file_two = open(filename_two, 'r')
    while True:
        line = file_two.readline()
        if not line:
            break
        result.add(line.strip())
    file_two.close()

    file_three = open(filename_three, 'r')
    while True:
        line = file_three.readline()
        if not line:
            break
        result.add(line.strip())
    file_three.close()

    file_out = open(filename_out, 'w')
    for item in result:
        file_out.write(str(item) + '\n')
    file_out.close()


if __name__ == '__main__':
    print()