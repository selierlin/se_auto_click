# encoding:utf-8

import json
import os


config = {}


def load_config():
    global config
    config_path = f'{get_root()}/config.json'
    if not os.path.exists(config_path):
        raise Exception('配置文件不存在，请根据config-template.json模板创建config.json文件')

    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = json.loads(config_str)
    print("载入config.json")
    return config


def get_root():
    return os.path.dirname(os.path.abspath(__file__))


def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def conf():
    return config


load_config()

if __name__ == '__main__':
    # load_config()
    print(get_root())