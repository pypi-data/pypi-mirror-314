def remove_empty_lines_from_list(list):
    return [x for x in list if x]


def print_list(list):
    for item in list:
        print(item)

def write_list_to_file(file_name, lines):
    with open(file_name, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def read_list_from_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]
