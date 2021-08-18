"""
Verify blockchain certificates (http://www.blockcerts.org/)

Overview of verification steps
- Check integrity: TODO: json-ld normalizatio
- Check signature (pre-v2)
- Check whether revoked
- Check whether expired
- Check authenticity

"""
import json

from cert_core import to_passport_model
from pspt_verifier import connectors
from pspt_verifier.checks import create_verification_steps
import sys


def verify_passport(passport_model, options={}):
    # lookup issuer-hosted information
    issuer_info = connectors.get_issuer_info(passport_model)

    # lookup transaction information
    connector = connectors.createTransactionLookupConnector(passport_model.chain, options)
    transaction_info = connector.lookup_tx(passport_model.txid)

    # create verification plan
    verification_steps = create_verification_steps(passport_model, transaction_info, issuer_info,
                                                   passport_model.chain)

    verification_steps.execute()
    messages = []
    verification_steps.add_detailed_status(messages)
    for message in messages:
        print(message['name'] + ',' + str(message['status']))

    return messages


def verify_passport_file(passport_file_name, transaction_id=None, options={}):
    with open(passport_file_name, 'rb') as pspt_fp:
        passport_bytes = pspt_fp.read()
        passport_json = json.loads(passport_bytes.decode('utf-8'))
        passport_model = to_passport_model(passport_json=passport_json,
                                                       txid=transaction_id,
                                                       passport_bytes=passport_bytes)
        result = verify_passport(passport_model, options)
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for cert_file in sys.argv[1:]:
            print(pspt_file)
            result = verify_passport_file(pspt_file)
            print(result)
    else:
        result = verify_passport_file('../tests/data/2.0/valid.json')
        print(result)
