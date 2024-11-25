import os, json

def json_load(json_path, encoding='utf-8', none_data={}):
    if os.path.isfile(json_path):
        with open(json_path, mode='r', encoding=encoding) as json_file:
            json_data = json.load(json_file)
            return json_data
    else:
        return none_data
    
def json_dump(json_path, data, encoding='utf-8'):
    json_dump = json.dumps(data, indent='\t', ensure_ascii=False)
    file = open(json_path, 'w', encoding=encoding)
    file.write(json_dump)
    file.close()