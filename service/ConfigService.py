import os
import yaml

def load(path):
    with open(path) as config_file:
        config = yaml.safe_load(config_file)
    return config


def get_connection_string(path):
    config = load(path)

    host = str(config['db']['host'])
    port = str(config['db']['port'])
    user = str(config['db']['user'])
    password = str(config['db']['password'])
    name = str(config['db']['name'])

    return 'postgresql+psycopg2://'+user+':'+password+'@'+host+':'+port+'/'+name

