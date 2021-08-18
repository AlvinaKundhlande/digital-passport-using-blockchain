#!/usr/bin/python3
import json
from flask import Flask, jsonify, request, abort
from subprocess import call

import pspt_issuer.config
from pspt_issuer.blockchain_handlers import bitcoin
import pspt_issuer.issue_passports

app = Flask(__name__)
config = None

def get_config():
    global config
    if config == None:
        config = pspt_issuer.config.get_config()
    return config

@app.route('/pspt_issuer/api/v1.0/issue', methods=['POST'])
def issue():
    config = get_config()
    passport_batch_handler, transaction_handler, connector = \
            bitcoin.instantiate_blockchain_handlers(config, False)
    passport_batch_handler.set_passports_in_batch(request.json)
    pspt_issuer.issue_passports.issue(config, passport_batch_handler, transaction_handler)
    return json.dumps(passport_batch_handler.proof)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
