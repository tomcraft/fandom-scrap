import os.path, json

def save_to_file(data, file):
    with open(file, 'w') as outfile:
        outfile.write(json.dumps(data))

def load_from_file(file):
    if (os.path.isfile(file)):
        with open(file, 'r') as openfile:
            return json.load(openfile)
    return None

def save_block_list(data):
    save_to_file(data, 'block_list.json')

def load_block_list():
    return load_from_file('block_list.json')

def save_detailed_block_list(data):
    save_to_file(data, 'detailed_block_list.json')

def load_detailed_block_list():
    return load_from_file('detailed_block_list.json')
