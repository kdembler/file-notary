import os
import logging
import json
import multiprocessing as mp
from web3 import Web3, HTTPProvider
from cobra_hdwallet import HDWallet


def _get_infura_web3():
    infura_endpoint = os.getenv("INFURA_ENDPOINT")
    chain_id = os.getenv("CHAIN_ID")

    if infura_endpoint is None:
        raise Exception("Endpoint not defined in the env")
    if chain_id is None:
        raise Exception("Chain id not defined in the env")

    return Web3(HTTPProvider(infura_endpoint))


def _load_contract_info(w3):
    with open('eth/fileNotary.json') as json_file:
        contract = json.load(json_file)
    notary = w3.eth.contract(
        address=contract['address'],
        abi=contract['abi']
    )
    return notary


def _init_web3():
    logger = logging.getLogger('eth')
    w3 = _get_infura_web3()
    if not w3.isConnected():
        raise Exception('web3 did not connect')
    logger.info('web3 connected')
    contract = _load_contract_info(w3)
    return w3, contract


def start_notary():
    w3, contract = _init_web3()
    # TODO: move to .env
    with open('eth/.pub') as pub_file:
        address = pub_file.readline().strip()

    with open('eth/.secret') as secret_file:
        mnemonic = secret_file.readline().strip()
    hd_wallet = HDWallet()
    account = hd_wallet.create_hdwallet(mnemonic)
    private_key = bytearray.fromhex(account['private_key'])
    notary_queue = mp.Queue()
    p = mp.Process(target=_notary_runner, args=(w3, contract, address, private_key, notary_queue))
    p.start()
    return notary_queue


def _notary_runner(w3, contract, address, private_key, queue):
    logger = logging.getLogger('eth')
    logger.info('starting queue processing')
    while True:
        logger.info('waiting for data to process')
        file_name, file_hash = queue.get()

        try:
            nonce = w3.eth.getTransactionCount(address)
            logger.info(f'notarizing {file_name} with hash {file_hash} and nonce {nonce}')
            txn = contract.functions.setFileHash(file_name, file_hash).buildTransaction({
                'from': address,
                'nonce': nonce
            })

            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            logger.info(f'transaction {txn_hash.hex()} sent')
        except Exception as e:
            logger.error(f'failed to notarize {file_name}: {e}')
