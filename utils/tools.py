import os
def get_input(day, sep ="\n", file_path = None):
    if not file_path:
        file_path = os.path.join('..', 'inputs', f'{day}.txt')
    with open(file_path, 'r') as f:
        input_file = [line.replace(sep,'') for line in f.readlines()]
    # print(input_file)
    return input_file