def generate_report(repository, tree):    
    print_totalization(tree)
    print_structure(repository, tree)

def print_totalization(tree):
    items = group_by_type(tree)
    total_rows = items['total_rows']
    total_bytes = items['total_bytes']
    
    print('')
    print(f'Total de linhas: { total_rows }')
    print(f'Total de bytes : { total_bytes }')
    print('')
    
    print('|-------------------------------------------------------------------|')
    print('| Extensão      |         Linhas          |          Bytes          |')
    print('|---------------|-------------------------|-------------------------|')
    
    for item in items:
        if item in ('total_rows', 'total_bytes'):
            continue

        space = ' ' * (14 - len(item))
        extension = item + space

        row_count = get_extension_data(total_rows, items[item]['row_count'])
        space = ' ' * (24 - len(row_count))
        row_count = space + row_count

        byte_count = get_extension_data(total_bytes, items[item]['byte_count'])
        space = ' ' * (24 - len(byte_count))
        byte_count = space + byte_count

        print(f'| {extension}|{row_count} |{byte_count} |')
    print('|-------------------------------------------------------------------|')

def group_by_type(tree):
    output = {    
        'total_rows': 0,
        'total_bytes': 0
    }
    
    for item in tree:
        is_file = 'path' in tree[item]

        if is_file:
            file_extension, row_count, byte_count = process_file(tree, item)
            
            output['total_rows'] += row_count
            output['total_bytes'] += byte_count

            if file_extension not in output:
                output[file_extension] = {
                    'row_count': 0,
                    'byte_count': 0,
                }
            
            output[file_extension]['row_count'] += row_count
            output[file_extension]['byte_count'] += byte_count
        else:
            subset = group_by_type(tree[item])
            output = merge_results(output, subset)

    
    return output

def process_file(tree, file_name):
    chuncks = file_name.split('.')
    if len(chuncks) > 0:
        file_extension = chuncks[-1]
    else:
        file_extension = 'outros'
    
    file_extension = file_extension.lower()
    row_count = tree[file_name]['row_count']
    byte_count = tree[file_name]['byte_count']

    return file_extension, row_count, byte_count

def merge_results(current, new):
    for item in new:
        if item in ('total_rows', 'total_bytes'):
            current[item] += new[item]
        else:
            if item not in current:
                current[item] = {
                    'row_count': 0,
                    'byte_count': 0,
                }

            current[item]['row_count'] += new[item]['row_count']
            current[item]['byte_count'] += new[item]['byte_count']
    
    return current

def get_extension_data(total, count):
    percent = (count * 100) / total
    percent = f'{percent:3.2f}'
    return f'{count} ({percent} %)'

def print_structure(repository, tree):
    print('')
    print(f'[{repository}]')
    print_structure_level(1, tree)
    print('')

def print_structure_level(level, tree):
    for item in tree:
      prefix = get_level_prefix(level)
      print(f'{prefix}[{item}]')
      
      is_directory = 'path' not in tree[item]
      if is_directory:
          print_structure_level(level + 1, tree[item])

def get_level_prefix(level):
    prefix = '|__ '
    for i in range(1, level):
        prefix = '|   ' + prefix

    return prefix