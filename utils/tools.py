import os
def get_input(day):
    file_path = os.path.join('..', 'inputs', f'{day}.txt')
    with open(file_path, 'r') as f:
        input_file = [line.replace('\n','') for line in f.readlines()]
    # print(input_file)
    return input_file