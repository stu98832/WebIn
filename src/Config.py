import json
import copy

__config =  { }

DEFAULT = {
    'notify': {
        'max-count': 3,
        'duration': 15000,
        'alive-time': 180000
    }
}

def LoadDefault():
    global __config

    __config = copy.deepcopy(DEFAULT)

def LoadFromJson(filename):
    global __config

    try:
        with open(filename, 'r+', encoding='utf-8') as f:
            __config = json.load(f)
        return True
    except:
        print('faild to load config file, default loaded')
        return False
        # TODO: Log

def SaveToJson(filename):
    try:
        with open(filename, 'w+', encoding='utf-8') as f:
            json.dump(__config, f, indent=4)
    except:
        print('faild to save config file')
        # TODO: Log

def Get(name):
    return __config[name] if name in __config else None

def Set(name, value):
    __config[name] = value