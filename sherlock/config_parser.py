import json

CONFIG = json.loads(
    open('sherlock/resources/config.json', 'r').read()
)

def get_config(section='', key=None, default=None):

    sectionPath = section.split('.')
    val = CONFIG
    
    for index, ss in enumerate(sectionPath):
        val = val.get(ss)
        if val == None:
            break
        if index == len(sectionPath)-1:
            val = val.get(key)

    return val or default


if __name__ == '__main__':
    print(get_config('storage', 'log_file', 'returnDefaultValue'))