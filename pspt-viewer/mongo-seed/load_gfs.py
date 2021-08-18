#!/usr/bin/env
'''
Loads passports to the mongodb used so that they are available from the pspt-viewer flask app when using gridfs.

Note that pspt_store_path option is used to find the passports.
'''
import glob
import gridfs
import configargparse
from pymongo import MongoClient
import os


def load_gridfs(config):
    mongodb_uri = config.mongodb_uri
    client = MongoClient(host=mongodb_uri)
    conn = client[mongodb_uri[mongodb_uri.rfind('/') + 1:len(mongodb_uri)]]

    fs = gridfs.GridFS(conn)

    pspt_glob = os.path.join(config.pspt_store_path, '*.json')
    json_files = glob.glob(cert_glob)

    for f in json_files:
        with open(f) as infile:
            filename = os.path.basename(f)
            content = infile.read()
            fs.put(content, filename=filename, encoding='utf-8')
            out = fs.find_one({'filename': filename})
            print('filename: ' + filename)
            print(out.read())


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')]) 
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('-m', '--mongodb_uri', type=str, default='mongodb://localhost:27017/test', help='the mongo DB to load the passports')
    p.add_argument('-s', '--pspt_store_path', type=str, default='.', help='the path where the passports can be found')
    args, _ = p.parse_known_args()

    return args



if __name__ == "__main__":
    conf = get_config()
    load_gridfs(conf)
